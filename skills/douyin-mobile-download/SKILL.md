---
name: douyin-mobile-download
description: 下载抖音公开单条视频到本地。用于用户提供抖音链接、分享文案或视频 ID 并要求保存视频；通过手机浏览器页面解析，支持 modal_id 搜索链接。不用于搜索视频、批量抓取主页或视频剪辑。
---

# 抖音手机页下载

使用 `scripts/download.py`，不要仅凭 HTTP 200 或解析器的 success 字段宣称成功。脚本核对作品 ID、流式下载并用 ffprobe/ffmpeg 检查文件；输出 JSON 和非零失败退出码。

## 已验证的方法

用 Playwright 的 iPhone 13 配置访问 `https://www.douyin.com/video/<ID>`，允许跳转到 `m.douyin.com/share/video/<ID>`，从页面 `_ROUTER_DATA` 读取对应作品及播放地址。标准入口失败时尝试手机直达入口。不要只依赖 `iesdouyin.com`：同一视频在那里可能返回错误页。

2026-09-26 在 Windows + Edge 的全新、未登录会话中成功下载 `7621879784973062134`（桃樂絲，琵琶曲双人舞，27.83 秒，720×1280，含音轨）。这是一次实测，不保证其他视频、网络或未来接口仍有效。Linux 代码路径使用 Chromium，需要在目标 Linux 环境复测。

Linux 上如果 Chromium 报 `net::ERR_SSL_PROTOCOL_ERROR` 或 TLS `wrong version number`，说明当前环境到抖音的 HTTPS 握手失败。先检查服务器的出站 HTTPS、代理配置和 TLS 中间设备；这不是作品 ID 或页面解析错误，也不能据此判断视频已删除。下载器会返回明确的网络错误，不应反复切换页面入口或把失败报告成泛化的 `Error`。

## 准备

在技能目录中建立隔离环境（不要覆盖用户现有环境）：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Linux 若缺浏览器系统库，使用 `python -m playwright install --with-deps chromium`；安装系统依赖遵循所在环境权限。还需要 PATH 中有 `ffmpeg` 和 `ffprobe`，Ubuntu/Debian 可通过包管理器安装 `ffmpeg`。

Windows 激活命令为 `.venv\Scripts\Activate.ps1`。已有 Edge 时加 `--channel msedge`，可省去 Chromium 下载。

## 执行

相对脚本路径以技能目录为基准，输出目录以运行时工作目录为基准。优先尊重用户指定输出位置；未指定时用任务目录的 `downloads`。

```bash
python scripts/download.py '抖音链接、分享文案或视频ID' --output-dir ./downloads
```

例如（Linux）：

```bash
python scripts/download.py 'https://www.douyin.com/video/7621879784973062134' --output-dir ./downloads
```

Windows 使用现有 Edge：

```powershell
python scripts/download.py 7621879784973062134 --channel msedge --output-dir ./downloads
```

支持 `v.douyin.com` 短链、`/video/<ID>`、手机分享页、`?modal_id=<ID>` 和分享文案。解析搜索链接时只取 modal_id 对应视频，不下载其他搜索结果。已有同名视频会重新校验并标记 reused，不覆盖。脚本默认不读取已有浏览器配置或登录 Cookie。

## 结果与失败处理

- 成功后给出实际文件链接、时长、尺寸；不要将解析成功当作下载成功，不保证无水印或原画。
- 正常流程最多尝试两个页面入口，遇到验证码停止该入口，不自动解验证码。若需要登录，告知用户当前匿名方法失败，不无限重试。
- 若返回 ID 不符、只有图文、没有媒体地址或解码失败，不交付为成功视频。失败的未完成文件保留为 `.part` 便于诊断。
- ffmpeg/ffprobe 缺失先补依赖；网络/TLS、DNS、超时、验证码、视频不可用分别按实际错误说明，不能直接推断视频已删除。浏览器异常只输出安全的错误分类，不输出带签名的媒体地址或会话信息。
- 不向聊天输出临时签名媒体 URL、Cookie 或会话信息。脚本仅保存最小元数据，不保存登录信息。
