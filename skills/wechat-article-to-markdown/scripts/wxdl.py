# -*- coding: utf-8 -*-
"""
微信公众号视频下载器
=====================
用 Playwright 加载文章、拦截视频请求、用浏览器会话下载。

功能:
  - 抓取文章标题 + 发布日期
  - 自动识别文章内多个视频
  - 分片 Range 下载, 选最高清晰度
  - 文件命名: YYYYMMDD_标题[_序号].mp4

用法:
  python wxdl.py <文章URL> [-o 输出目录] [--format json|text]

作者: LH (2026)
"""
import argparse
import json
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 "
    "Mobile/15E148 Safari/604.1"
)

# ---------- 工具函数 ----------

INVALID_FS_CHARS = re.compile(r'[\\/:*?"<>|\r\n\t]')

def safe_filename(name: str, max_len: int = 80) -> str:
    """去掉文件名里 Windows 非法字符, 截断超长"""
    if not name:
        return "wx_video"
    s = INVALID_FS_CHARS.sub("_", name).strip().strip(".")
    s = re.sub(r"\s+", " ", s)
    if len(s) > max_len:
        s = s[:max_len].rstrip()
    return s or "wx_video"

def is_video_url(u: str) -> bool:
    return bool(re.match(r"^https?://mpvideo\.qpic\.cn/[^?]+\.mp4", u))

def video_id(u: str) -> str:
    """把同一个视频的不同清晰度归到一个 id"""
    m = re.match(r"^https?://mpvideo\.qpic\.cn/([^.]+)\.", u)
    return m.group(1) if m else u

def format_rank(u: str) -> int:
    """f10104 > f10102 > f10004 > f10002 (值越大清晰度越高)"""
    m = re.search(r"\.f(\d+)\.", u)
    return int(m.group(1)) if m else 0

def extract_meta(html: str):
    """从文章 HTML 里抠出标题和发布日期(YYYYMMDD)"""
    # 标题
    title = None
    for pat in (
        r'var\s+msg_title\s*=\s*["\']([^"\']+)',
        r'<meta\s+property="og:title"\s+content="([^"]+)"',
        r'<title>([^<]+)</title>',
    ):
        m = re.search(pat, html)
        if m:
            title = m.group(1).strip()
            break

    # 发布日期 (公众号页面通常有 publish_time 或 var t=)
    date_str = None
    m = re.search(r'var\s+ct\s*=\s*["\'](\d{10})', html)  # 秒级时间戳
    if m:
        ts = int(m.group(1))
        date_str = time.strftime("%Y%m%d", time.localtime(ts))
    if not date_str:
        m = re.search(r'publish_time["\']?\s*[:=]\s*["\']?(\d{4}-\d{2}-\d{2})', html)
        if m:
            date_str = m.group(1).replace("-", "")
    if not date_str:
        # 页面里可能有 "2026年7月9日" 之类
        m = re.search(r"(\d{4})[年\-/](\d{1,2})[月\-/](\d{1,2})", html)
        if m:
            y, mo, d = m.groups()
            date_str = f"{int(y):04d}{int(mo):02d}{int(d):02d}"
    if not date_str:
        date_str = time.strftime("%Y%m%d")  # 兜底: 今天

    return (title or "wx_article"), date_str


# ---------- 下载核心 ----------

def range_download(req_ctx, url, out_path, referer, ua, log=print):
    """分片 Range 下载, 每片 1MB, 失败重试 3 次"""
    hdrs_base = {
        "Referer": referer,
        "User-Agent": ua,
        "Accept": "*/*",
        "Accept-Encoding": "identity",
    }
    # 探测总大小
    r0 = req_ctx.get(
        url, headers={**hdrs_base, "Range": "bytes=0-0"}, timeout=60000
    )
    if r0.status not in (200, 206):
        return False, f"探测失败 HTTP {r0.status}", 0
    cr = r0.headers.get("content-range") or r0.headers.get("Content-Range") or ""
    total = None
    if "/" in cr:
        try:
            total = int(cr.split("/")[-1])
        except Exception:
            pass
    if not total:
        cl = r0.headers.get("content-length") or r0.headers.get("Content-Length")
        total = int(cl) if cl else None
    if not total:
        return False, "拿不到总大小", 0

    CHUNK = 1024 * 1024
    with open(out_path, "wb") as f:
        pos = 0
        retry = 0
        while pos < total:
            end = min(pos + CHUNK - 1, total - 1)
            hdrs = {**hdrs_base, "Range": f"bytes={pos}-{end}"}
            try:
                r = req_ctx.get(url, headers=hdrs, timeout=60000)
                if r.status not in (200, 206):
                    raise RuntimeError(f"HTTP {r.status}")
                body = r.body()
                f.write(body)
                pos += len(body)
                retry = 0
                pct = pos * 100 / total
                sys.stdout.write(
                    f"\r    下载中 {pos/1048576:.2f}/{total/1048576:.2f} MB ({pct:.1f}%)"
                )
                sys.stdout.flush()
            except Exception as e:
                retry += 1
                if retry > 3:
                    return False, f"重试失败 @ pos={pos}: {e}", pos
                time.sleep(1)
    sys.stdout.write("\n")
    return True, "ok", total


# ---------- 主流程 ----------

def run(article_url: str, out_dir: str, verbose=True):
    log = print if verbose else (lambda *a, **k: None)

    captured = []       # [{url, status}]
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE"),
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=MOBILE_UA,
            viewport={"width": 414, "height": 896},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        page = ctx.new_page()

        def on_response(resp):
            u = resp.url
            if is_video_url(u) and u not in seen:
                seen.add(u)
                captured.append({"url": u, "status": resp.status})
                log(f"  [捕获] {resp.status} f{format_rank(u)} {u[:100]}...")

        page.on("response", on_response)

        log(f"[1] 打开文章: {article_url}")
        page.goto(article_url, timeout=60000, wait_until="domcontentloaded")

        # 抓标题 + 日期
        html = page.content()
        title, date_str = extract_meta(html)
        log(f"    标题: {title}")
        log(f"    日期: {date_str}")

        log("[2] 滚动 + 触发所有 video 元素播放")
        page.wait_for_timeout(1500)
        # 反复滚动到底部, 触发懒加载视频
        for _ in range(6):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(700)
        # 强制播放所有 <video>
        page.evaluate("""() => {
            document.querySelectorAll('video').forEach(v => {
                try { v.muted = true; v.play(); } catch(e) {}
            });
        }""")

        log("[3] 等待视频响应(20s)")
        deadline = time.time() + 20
        stable_since = None
        last_count = 0
        while time.time() < deadline:
            page.wait_for_timeout(800)
            if len(captured) != last_count:
                last_count = len(captured)
                stable_since = time.time()
            elif captured and stable_since and time.time() - stable_since > 4:
                # 4 秒没有新视频, 认为都发现完了
                break

        if not captured:
            log("!! 未捕获到视频")
            browser.close()
            return {"ok": False, "error": "no_video_found", "title": title, "date": date_str}

        # 按视频 id 分组, 每组取最高清
        groups = {}
        for c in captured:
            vid = video_id(c["url"])
            if vid not in groups or format_rank(c["url"]) > format_rank(groups[vid]["url"]):
                groups[vid] = c
        picks = list(groups.values())
        # 按 id 稳定排序 (文章里的出现顺序)
        picks.sort(key=lambda x: [c["url"] for c in captured].index(x["url"]))

        log(f"[4] 共 {len(picks)} 个不同视频, 逐个下载")

        os.makedirs(out_dir, exist_ok=True)
        req_ctx = ctx.request
        results = []

        base_name = f"{date_str}_{safe_filename(title)}"
        for i, c in enumerate(picks, 1):
            url = c["url"]
            if len(picks) == 1:
                fname = f"{base_name}.mp4"
            else:
                fname = f"{base_name}_{i}.mp4"
            out_path = os.path.join(out_dir, fname)

            log(f"  [{i}/{len(picks)}] f{format_rank(url)} -> {fname}")
            ok, info, size = range_download(
                req_ctx, url, out_path, article_url, MOBILE_UA, log
            )
            if ok:
                log(f"    完成: {size/1048576:.2f} MB")
                results.append({
                    "ok": True,
                    "file": os.path.abspath(out_path),
                    "size": size,
                    "url": url,
                })
            else:
                log(f"    失败: {info}")
                if os.path.exists(out_path):
                    os.remove(out_path)
                results.append({"ok": False, "error": info, "url": url})

        browser.close()
        return {
            "ok": all(r["ok"] for r in results),
            "title": title,
            "date": date_str,
            "count": len(results),
            "results": results,
        }


def main():
    ap = argparse.ArgumentParser(
        description="微信公众号视频下载器 (支持一篇多视频)"
    )
    ap.add_argument("url", help="公众号文章 URL (mp.weixin.qq.com/s/...)")
    ap.add_argument("-o", "--out-dir", default=".", help="输出目录 (默认当前)")
    ap.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式: text (默认) 或 json",
    )
    args = ap.parse_args()

    quiet = args.format == "json"
    result = run(args.url, args.out_dir, verbose=not quiet)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print()
        if result["ok"]:
            print(f"[OK] 全部完成, 共 {result['count']} 个视频")
            for r in result["results"]:
                if r["ok"]:
                    print(f"     -> {r['file']}  ({r['size']/1048576:.2f} MB)")
        else:
            print("[FAIL] 部分或全部失败")
            for r in result["results"]:
                if not r["ok"]:
                    print(f"     x {r.get('error')}")
    sys.exit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()

