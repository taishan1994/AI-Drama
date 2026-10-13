# -*- coding: utf-8 -*-
"""
wxdl-full - 微信公众号"正文+图片URL+视频"一体化下载 (联动两个 skill)

流程:
  1. 抓文章 HTML (mobile UA)
  2. 复用 wechat-article-downloader 的 fetch_article.py 出正文 md
     (自己再抓一遍 HTML, 把视频位置替换成占位 <!--WXVIDEO-N-->)
  3. 复用 wx-video-downloader 的 wxdl.py 下 mp4
  4. 用本地 mp4 相对路径回填占位

输出:
  <out-dir>/<YYYYMMDD_标题>/
      <YYYYMMDD_标题>.md
      <YYYYMMDD_标题>[_1_2].mp4

用法:
  python wxdl_full.py <文章URL> [-o 输出根目录]
"""
import argparse
import os
import re
import subprocess
import sys
import time
import urllib.request

# 复用 wxdl.py 里的东西
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from wxdl import (
    MOBILE_UA, extract_meta, safe_filename,
    is_video_url, format_rank, video_id, range_download,
)
from playwright.sync_api import sync_playwright

# ---------- HTML → Markdown (含视频占位) ----------

def html_to_markdown_with_video(html: str) -> str:
    """在 html_to_markdown 基础上, 把视频 iframe / mpvoice 替换成占位标记"""
    # 移除 script / style (但保留视频 iframe)
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)

    # 找出所有视频占位, 换成 @@WXVIDEO-N@@
    # 微信文章视频结构:
    #   <iframe class="video_iframe" data-mpvid="wxv_xxx" data-cover="URL编码的jpg" ...>
    vid_pat = re.compile(
        r'<iframe[^>]*data-mpvid="(wxv_[0-9a-zA-Z]+)"[^>]*>.*?</iframe>',
        flags=re.DOTALL | re.IGNORECASE,
    )
    vids_in_order = []       # [(vid, cover_url_or_None), ...]
    def _sub_video(m):
        block = m.group(0)
        vid = m.group(1)
        # 抠出 data-cover (URL 编码的封面图地址)
        cover_url = None
        cm = re.search(r'data-cover="([^"]+)"', block)
        if cm:
            import urllib.parse
            cover_url = urllib.parse.unquote(cm.group(1))
        vids_in_order.append((vid, cover_url))
        # 用不含 < > 的占位, 避免被后面 re.sub(r"<[^>]+>", "", ...) 吃掉
        return f"\n\n@@WXVIDEO-{len(vids_in_order)}@@\n\n"
    html = vid_pat.sub(_sub_video, html)

    # 图片
    def extract_img(m):
        src = ""
        for attr in ["data-src", "src", "data-croporisrc"]:
            v = re.search(rf'{attr}="([^"]+)"', m.group(0))
            if v:
                src = v.group(1); break
        alt = ""
        alt_m = re.search(r'alt="([^"]*)"', m.group(0))
        if alt_m: alt = alt_m.group(1)
        return f"![{alt}]({src})" if src else ""
    html = re.sub(r"<img[^>]+>", extract_img, html)

    # 块级标签换行
    for tag in ["section", "div", "p", "h1", "h2", "h3", "h4", "h5", "h6",
                "li", "tr", "blockquote"]:
        html = re.sub(rf"<{tag}[^>]*>", "\n", html)
        html = re.sub(rf"</{tag}>", "\n", html)
    html = re.sub(r"<br\s*/?>", "\n", html)
    for tag in ["ol", "ul"]:
        html = re.sub(rf"<{tag}[^>]*>", "\n", html)
        html = re.sub(rf"</{tag}>", "\n", html)

    html = re.sub(r"<(?:strong|b)[^>]*>", "**", html)
    html = re.sub(r"</(?:strong|b)>", "**", html)
    html = re.sub(r"<(?:em|i)[^>]*>", "*", html)
    html = re.sub(r"</(?:em|i)>", "*", html)

    def extract_link(m):
        href = m.group(1); text = m.group(2) or ""
        return f"[{text}]({href})" if (href and text) else (text or href)
    html = re.sub(
        r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        extract_link, html, flags=re.DOTALL,
    )
    html = re.sub(r"<a[^>]*>(.*?)</a>", r"\1", html)
    html = re.sub(r"<span[^>]*>", "", html); html = re.sub(r"</span>", "", html)
    html = re.sub(r"<[^>]+>", "", html)

    entities = {"&amp;": "&", "&lt;": "<", "&gt;": ">",
                "&quot;": '"', "&#39;": "'", "&nbsp;": " "}
    for k, v in entities.items(): html = html.replace(k, v)

    lines = [line.strip() for line in html.split("\n")]
    result, prev_empty = [], False
    for line in lines:
        if line == "":
            if not prev_empty: result.append(""); prev_empty = True
        else:
            result.append(line); prev_empty = False
    return "\n".join(result).strip(), vids_in_order


# ---------- 主流程 ----------

def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": MOBILE_UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def _guess_ext(url: str, content_type: str = "") -> str:
    """从 URL 或 Content-Type 猜文件扩展名"""
    ct = (content_type or "").lower()
    if "png" in ct: return ".png"
    if "gif" in ct: return ".gif"
    if "webp" in ct: return ".webp"
    if "jpeg" in ct or "jpg" in ct: return ".jpg"
    # 从 URL 猜
    m = re.search(r"wx_fmt=(\w+)", url)
    if m:
        fmt = m.group(1).lower()
        return "." + ("jpg" if fmt == "jpeg" else fmt)
    for ext in (".png", ".gif", ".webp", ".jpeg", ".jpg"):
        if ext in url.lower(): return ext
    return ".jpg"


def download_image(url: str, out_dir: str, filename: str) -> str:
    """下一张图, 返回本地文件相对路径; 失败返回空"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": MOBILE_UA,
            "Referer": "https://mp.weixin.qq.com/",
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            ct = r.headers.get("Content-Type", "")
            ext = _guess_ext(url, ct)
            fname = filename + ext
            path = os.path.join(out_dir, fname)
            with open(path, "wb") as f:
                f.write(r.read())
            return fname
    except Exception as e:
        print(f"      [图片下载失败] {e}  {url[:80]}")
        return ""


def localize_images(md_body: str, cover_url: str, images_dir: str,
                    images_subdir_name: str = "images"):
    """
    把 md 里所有远程图片下到本地 images_dir, 返回:
      (改写后的 md_body, 改写后的 cover_local_relpath, 计数)
    - 保留原 URL 作为脚注引用, 双保险
    """
    os.makedirs(images_dir, exist_ok=True)

    # 收集所有出现的 URL (顺序 + 去重)
    urls_in_order = []
    seen = set()
    for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", md_body):
        u = m.group(2)
        if u.startswith("http") and u not in seen:
            seen.add(u); urls_in_order.append(u)

    # 逐个下载, 得到 URL → 本地相对路径 的映射
    url2local = {}
    for i, url in enumerate(urls_in_order, 1):
        print(f"    [图 {i}/{len(urls_in_order)}] 下载 {url[:80]}...")
        local = download_image(url, images_dir, f"img_{i:02d}")
        if local:
            url2local[url] = f"{images_subdir_name}/{local}"

    # 改写 MD 里的图片引用
    def _replace_img(m):
        alt, url = m.group(1), m.group(2)
        if url in url2local:
            return f"![{alt}]({url2local[url]})"
        return m.group(0)  # 保留原样
    md_body = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _replace_img, md_body)

    # 封面
    cover_local = ""
    if cover_url:
        print(f"    [封面] 下载 {cover_url[:80]}...")
        cover_fname = download_image(cover_url, images_dir, "cover")
        if cover_fname:
            cover_local = f"{images_subdir_name}/{cover_fname}"

    return md_body, cover_local, len(url2local)


def download_videos(article_url: str, out_dir: str, verbose=True):
    """复用 wxdl 核心 - 返回 [{ok, file, url}]"""
    captured = []; seen = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE"),
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=MOBILE_UA,
            viewport={"width": 414, "height": 896},
            device_scale_factor=2, is_mobile=True, has_touch=True,
        )
        page = ctx.new_page()
        def on_response(resp):
            u = resp.url
            if is_video_url(u) and u not in seen:
                seen.add(u); captured.append({"url": u, "status": resp.status})
                if verbose:
                    print(f"    [捕获] f{format_rank(u)} {u[:80]}...")
        page.on("response", on_response)
        page.goto(article_url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
        for _ in range(6):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(700)
        page.evaluate("""() => {
            document.querySelectorAll('video').forEach(v => {
                try { v.muted = true; v.play(); } catch(e){}
            });
        }""")
        deadline = time.time() + 20; stable_since = None; last = 0
        while time.time() < deadline:
            page.wait_for_timeout(800)
            if len(captured) != last:
                last = len(captured); stable_since = time.time()
            elif captured and stable_since and time.time() - stable_since > 4:
                break
        if not captured:
            browser.close(); return []
        # 每个视频取最高清
        groups = {}
        for c in captured:
            vid = video_id(c["url"])
            if vid not in groups or format_rank(c["url"]) > format_rank(groups[vid]["url"]):
                groups[vid] = c
        picks = sorted(
            groups.values(),
            key=lambda x: [c["url"] for c in captured].index(x["url"])
        )
        # 下载
        req_ctx = ctx.request; results = []
        for i, c in enumerate(picks, 1):
            base = os.path.basename(out_dir)
            fname = f"{base}.mp4" if len(picks) == 1 else f"{base}_{i}.mp4"
            out_path = os.path.join(out_dir, fname)
            if verbose: print(f"    [{i}/{len(picks)}] 下载到 {fname}")
            ok, info, size = range_download(
                req_ctx, c["url"], out_path, article_url, MOBILE_UA,
                (lambda *a, **k: None) if not verbose else print,
            )
            if ok:
                results.append({"ok": True, "file": os.path.abspath(out_path),
                                "name": fname, "size": size, "url": c["url"]})
                if verbose: print(f"      完成 {size/1048576:.2f} MB")
            else:
                if os.path.exists(out_path): os.remove(out_path)
                results.append({"ok": False, "error": info, "url": c["url"]})
        browser.close()
        return results


def run(article_url: str, out_root: str):
    print(f"[1] 抓文章 HTML")
    html = fetch_html(article_url)
    title, date_str = extract_meta(html)
    base_name = f"{date_str}_{safe_filename(title)}"
    out_dir = os.path.join(out_root, base_name)
    os.makedirs(out_dir, exist_ok=True)
    print(f"    标题: {title}")
    print(f"    日期: {date_str}")
    print(f"    输出目录: {out_dir}")

    # ---- 正文 ----
    print("[2] 提取正文 (含视频占位标记)")
    # 用页面里 js_content 段
    content_match = re.search(
        r'id="js_content"[^>]*>(.*?)</div>\s*<(?:script|div)',
        html, re.DOTALL,
    )
    if not content_match:
        content_match = re.search(r'id="js_content"[^>]*>(.*)', html, re.DOTALL)
    if not content_match:
        print("!! 找不到正文"); return {"ok": False, "error": "no_content"}
    body_html = content_match.group(1)
    md_body, vids_in_order = html_to_markdown_with_video(body_html)
    print(f"    识别到 {len(vids_in_order)} 个视频占位: {vids_in_order}")

    # 封面 / 作者 / 时间
    cover = ""
    m = re.search(r'var msg_cdn_url = "([^"]+)"', html)
    if m: cover = m.group(1)
    author = ""
    m = re.search(r'var author_name = "([^"]+)"', html)
    if m: author = m.group(1)
    create_time = ""
    m = re.search(r'var create_time = "(\d+)"', html)
    if m:
        ts = int(m.group(1))
        create_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))

    # ---- 视频 ----
    print("[3] 下载视频 (Playwright)")
    videos = download_videos(article_url, out_dir, verbose=True)
    ok_videos = [v for v in videos if v.get("ok")]
    print(f"    下载成功 {len(ok_videos)}/{len(videos)}")

    # ---- 图片本地化 (含视频封面) ----
    print("[4] 下载所有图片到本地 images/")
    images_dir = os.path.join(out_dir, "images")
    md_body, cover_local, img_count = localize_images(md_body, cover, images_dir)

    # 单独下每个视频的封面图 (用作 MD 里的缩略图)
    video_poster_paths = []
    for i, (vid, poster_url) in enumerate(vids_in_order, 1):
        if poster_url:
            print(f"    [视频{i}封面] 下载 {poster_url[:80]}...")
            fname = download_image(poster_url, images_dir, f"video_{i:02d}_poster")
            video_poster_paths.append(f"images/{fname}" if fname else "")
        else:
            video_poster_paths.append("")
    print(f"    本地化 {img_count} 张图片"
          + (" + 1 张封面" if cover_local else "")
          + (f" + {sum(1 for p in video_poster_paths if p)} 张视频封面" if video_poster_paths else ""))

    # ---- 回填视频占位 (纯 Markdown 语法, 保证所有渲染器一致显示) ----
    print("[5] 回填视频到 Markdown")
    import urllib.parse as _up
    for i, (vid, _poster_url) in enumerate(vids_in_order, 1):
        marker = f"@@WXVIDEO-{i}@@"
        if i <= len(ok_videos):
            fname = ok_videos[i - 1]["name"]
            fname_url = _up.quote(fname)
            poster = video_poster_paths[i - 1] if i - 1 < len(video_poster_paths) else ""
            poster_url = _up.quote(poster) if poster else ""
            if poster:
                # 缩略图 + 可点击链接跳到 mp4, 所有 MD 渲染器通用
                thumb_md = f"[![视频{i} 点击播放]({poster_url})](./{fname_url})"
            else:
                thumb_md = f"▶️ [点击播放视频{i}](./{fname_url})"
            replacement = (
                f"{thumb_md}\n\n"
                f"> 🎬 [▶ 点击播放视频 {i}](./{fname_url})（在系统播放器中打开）"
            )
        else:
            replacement = f"*[视频 {i} 下载失败, vid={vid}]*"
        md_body = md_body.replace(marker, replacement)

    # ---- 组装 MD (全部本地引用) ----
    lines = [f"# {title}", ""]
    if author: lines.append(f"> **作者**：{author}")
    if create_time: lines.append(f"> **时间**：{create_time}")
    lines.append(f"> **来源**：[原文链接]({article_url})")
    lines.append("")
    if ok_videos:
        lines.append(f"> ⚠️ **本文含 {len(ok_videos)} 段视频。** Markdown 预览无法内嵌播放视频，"
                     f"如需「点一下就播」，请打开同目录的 **`{base_name}.html`**（浏览器），"
                     f"或直接双击目录里的 `.mp4` 文件。")
        lines.append("")
    if cover_local:
        lines.append(f"![封面](./{cover_local})")
        lines.append("")
    elif cover:
        lines.append(f"![封面]({cover})")
        lines.append("")
    lines.append("---"); lines.append("")
    lines.append(md_body)
    lines.append(""); lines.append("---"); lines.append("")
    lines.append(f"**原文链接**：<{article_url}>")
    if img_count or ok_videos:
        lines.append("")
        lines.append(f"**本地资源**：{img_count} 张图片 + {len(ok_videos)} 段视频，均已下载到本文件所在目录，双击 MD 即可完整阅读，无需联网。")

    md_path = os.path.join(out_dir, base_name + ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"    保存: {md_path}")

    # ---- 顺便生成一份自包含 HTML (视频真正内嵌播放) ----
    print("[6] 生成 HTML 版本 (视频内嵌播放)")
    html_path = os.path.join(out_dir, base_name + ".html")
    html_out = build_html(
        title=title, author=author, create_time=create_time,
        cover_local=cover_local, cover_url=cover,
        article_url=article_url,
        md_body_original=md_body,  # 此时 md_body 里视频占位已被 MD 缩略图语法替换
        ok_videos=ok_videos, video_posters=video_poster_paths,
        img_count=img_count,
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"    保存: {html_path}")

    return {
        "ok": True,
        "dir": os.path.abspath(out_dir),
        "md": os.path.abspath(md_path),
        "html": os.path.abspath(html_path),
        "videos": ok_videos,
        "images": img_count,
        "video_placeholders": len(vids_in_order),
    }


def build_html(*, title, author, create_time, cover_local, cover_url,
               article_url, md_body_original, ok_videos, video_posters,
               img_count):
    """把已经回填过缩略图占位的 md 转成简单 HTML, 视频真正内嵌 <video>"""
    import html as _html
    import urllib.parse as _up

    body = md_body_original

    # 1. 把 MD 里"缩略图 + quote 说明"格式还原成真正的 <video>
    #    格式: [![视频N 点击播放](poster_url)](./mp4_url)\n\n> 🎬 **视频 N**：...
    def _video_html_repl(m):
        i = int(m.group(1))
        if i - 1 < len(ok_videos):
            fname = ok_videos[i - 1]["name"]
            fname_url = _up.quote(fname)
            poster = video_posters[i - 1] if i - 1 < len(video_posters) else ""
            poster_url = _up.quote(poster) if poster else ""
            poster_attr = f' poster="./{poster_url}"' if poster else ''
            # preload="none": 只显示封面, 不预下载视频, 避免浏览器沙箱环境
            # 里 <video> 预加载被中止而产生 ERR_ABORTED 报错
            return (
                f'<video src="./{fname_url}" controls preload="none"{poster_attr} '
                f'style="max-width:100%;border-radius:6px;display:block;margin:20px auto;"></video>'
            )
        return m.group(0)
    body = re.sub(
        r'\[!\[视频(\d+)[^\]]*\]\([^)]+\)\]\([^)]+\)\s*\n+> [^\n]*',
        _video_html_repl, body,
    )

    # 2. 简单 MD → HTML 转换 (只处理常见语法)
    def _md_to_html(md):
        out_lines = []
        for line in md.split("\n"):
            # 已经是 HTML (<video><figure>) 就直接放
            if line.strip().startswith("<") and ">" in line:
                out_lines.append(line); continue
            # 图片
            line = re.sub(
                r'!\[([^\]]*)\]\(([^)]+)\)',
                lambda m: f'<img src="{m.group(2)}" alt="{_html.escape(m.group(1))}" '
                          f'style="max-width:100%;border-radius:6px;">',
                line,
            )
            # 链接
            line = re.sub(
                r'\[([^\]]+)\]\(([^)]+)\)',
                lambda m: f'<a href="{m.group(2)}">{_html.escape(m.group(1))}</a>',
                line,
            )
            # 加粗
            line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            out_lines.append(line)
        # 段落分隔
        text = "\n".join(out_lines)
        # 空行分段
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text)]
        html_parts = []
        for p in paragraphs:
            if not p: continue
            if p.startswith(("<video ", "<figure", "<hr", "<h1", "<h2", "<h3", "<h4", "<h5", "<h6", "<iframe", "<table", "<blockquote", "<div", "<section", "<pre", "<ol", "<ul", "<li")):
                html_parts.append(p)
            elif p.startswith("---"):
                html_parts.append("<hr>")
            else:
                html_parts.append(f"<p>{p}</p>")
        return "\n".join(html_parts)

    body_html = _md_to_html(body)

    cover_html = ""
    if cover_local:
        cover_html = f'<img class="cover" src="./{_up.quote(cover_local)}" alt="封面">'
    elif cover_url:
        cover_html = f'<img class="cover" src="{cover_url}" alt="封面">'

    meta_parts = []
    if author: meta_parts.append(f"<span>👤 {_html.escape(author)}</span>")
    if create_time: meta_parts.append(f"<span>🕒 {_html.escape(create_time)}</span>")
    meta_parts.append(f'<span>🔗 <a href="{article_url}" target="_blank">原文链接</a></span>')
    meta_html = " · ".join(meta_parts)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html.escape(title)}</title>
<style>
  /* 全局盒模型 */
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{ max-width: 720px; margin: 0 auto; padding: 24px 16px;
         font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
                      "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
         line-height: 1.75; color: #333; background: #fafafa;
         overflow-x: hidden; }}
  h1 {{ font-size: 24px; line-height: 1.4; margin: 12px 0 4px; }}
  .meta {{ color: #888; font-size: 13px; margin-bottom: 20px; }}
  .meta span {{ margin-right: 4px; }}
  /* 所有图片自适应容器, 绝不撑破页面 */
  img {{ display: block; margin: 12px auto; max-width: 100%; height: auto;
         border-radius: 6px; }}
  /* 封面按微信标准 2.35:1 显示 (cover fit 保证不变形不撑破) */
  img.cover {{ width: 100%; aspect-ratio: 2.35 / 1; object-fit: cover;
               margin: 0 0 20px 0; }}
  video {{ display: block; margin: 12px auto; max-width: 100%; height: auto;
          background: #000; border-radius: 6px; }}
  figure.video-block {{ margin: 20px 0; text-align: center; }}
  figcaption {{ font-size: 13px; color: #888; margin-top: 6px; }}
  p {{ margin: 12px 0; word-wrap: break-word; overflow-wrap: break-word; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 24px 0; }}
  a {{ color: #576b95; }}
  footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #ddd;
            color: #888; font-size: 13px; }}
</style>
</head>
<body>
<h1>{_html.escape(title)}</h1>
<div class="meta">{meta_html}</div>
{cover_html}
<hr>
{body_html}
<footer>
  <p><strong>原文链接</strong>：<a href="{article_url}" target="_blank">{article_url}</a></p>
  <p>本地资源：{img_count} 张图片 + {len(ok_videos)} 段视频，全部随本文件保存。</p>
</footer>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="微信公众号文章 全文+图片+视频 一体化下载")
    ap.add_argument("url", help="文章URL (mp.weixin.qq.com/s/...)")
    ap.add_argument("-o", "--out-root", default=".",
                    help="输出根目录 (默认当前目录；会在下面建 YYYYMMDD_标题/ 子目录)")
    args = ap.parse_args()
    result = run(args.url, args.out_root)
    print()
    if result.get("ok"):
        print(f"[OK] 完成 - 目录: {result['dir']}")
        print(f"     MD:   {result['md']}")
        print(f"     HTML: {result.get('html','')}   <- 视频真正内嵌播放, 双击浏览器打开")
        print(f"     图片: {result.get('images', 0)} 张 (本地化到 images/)")
        print(f"     视频占位 {result['video_placeholders']} 个, 成功下载 {len(result['videos'])} 个:")
        for v in result["videos"]:
            print(f"       - {v['file']}  ({v['size']/1048576:.2f} MB)")
    else:
        print(f"[FAIL] {result.get('error')}")
        sys.exit(2)


if __name__ == "__main__":
    main()
