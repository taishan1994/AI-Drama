# FreeVideo 本机安装与使用

记录日期：2026-10-07。通用说明见 [README.zh-CN.md](README.zh-CN.md)。

## 当前安装

| 项目 | 位置或状态 |
| --- | --- |
| FreeVideo | `/nfs/FM/gongoubo/new_project/github/aigc/FreeVideo` |
| GPU | NVIDIA GeForce RTX 5090，32 GB 显存 |
| 运行环境 | `envs/unified`，PyTorch 2.13.0+cu130 |
| 视频模型 | ConvRot int8，`models/vdn` |
| 文本编码器 | `models/encoder/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` |
| 模型下载偏好 | `download-settings.json` 中的 `source: modelscope` |
| ComfyUI 插件 | `../ComfyUI/custom_nodes/FreeVideo`，通过其 `comfyui.json` 指向本安装 |

安装器的 `machine.json` 已标记 `ready: true`，GPU 内核检查通过。模型下载记录显示 VDN 和绝大多数 Edge 文件从 ModelScope 校验完成；少量文件由安装器从 Hugging Face 官方源补齐。文本编码器另从 ModelScope 的 `Comfy-Org/MiniMax-H3` 下载，完整 SHA256 为 `35a88d51044231fe332301d7a62aa81e3f2cba62febeb446e2c1e3e0ef76f2c6`，与 FreeVideo 清单一致。

## 重装或修复

先阅读并自行确认 [MiniMax H3 模型许可证](https://huggingface.co/OpenVDN/vdn-minimax-h3/blob/751739ee5b9e3ac802dca5d5111075fdaeb47885/LICENSE)。该许可证对使用地域有限制。安装器的无人值守模式需要明确的 `--accept-model-license` 参数。

在 FreeVideo 目录执行：

```bash
cd /nfs/FM/gongoubo/new_project/github/aigc/FreeVideo
python3 -c 'from pathlib import Path; from freevideo_engine.download_settings import preference; preference(Path.cwd(), "modelscope")'
./setup.sh --plan --reuse-models ../ComfyUI/models
./setup.sh --yes --accept-model-license --plain --reuse-models ../ComfyUI/models
```

安装器会复用已验证的文件，失败后重跑同一命令即可继续。首次安装预估需下载约 52 GiB 模型，并为环境、缓存和模型预留约 100 GiB 空间。`--reuse-models` 在本机复用了 ComfyUI 中约 0.6 GiB 的潜空间放大模型。

ModelScope 没有被 FreeVideo 内置为文本编码器的下载源。本机使用 ModelScope 的同名文件，并在放入 `models/encoder/text_encoders/` 前按上述 SHA256 完整校验；重装时该文件仍在则安装器会复用。模型下载偏好只表示**优先**使用 ModelScope，安装器可能在部分文件上回退到官方源。

如果 PyPI 官方源下载依赖很慢，可用清华镜像安装运行依赖，再重跑 `setup.sh` 完成后续步骤：

```bash
UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple \
UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
UV_CACHE_DIR="$PWD/downloads/uv-cache" \
tools/uv-x86_64-unknown-linux-gnu/uv --no-config pip install \
  --python envs/unified/bin/python -e "$PWD[runtime]" \
  -c constraints/unified.txt pip ninja packaging wheel setuptools \
  -r constraints/encoder-runtime.txt
```

## ComfyUI 与命令行

现有 ComfyUI 插件的 `comfyui.json` 内容为：

```json
{
  "installation": "/nfs/FM/gongoubo/new_project/github/aigc/FreeVideo"
}
```

启动或重启 ComfyUI 后，在 **工作流 → 浏览模板 → FreeVideo → FreeVideo-All-in-One** 打开模板。命令行生成：

```bash
cd /nfs/FM/gongoubo/new_project/github/aigc/FreeVideo
./freevideo generate --prompt-file prompt.txt --out video.mp4
```

`prompt.txt` 为 UTF-8 文本提示词文件。可用 `./freevideo generate --help` 查看分辨率、时长等参数。

## 验证记录

安装完成后运行了一次 256×256、39 帧的文生视频与音频测试。结果为 [测试视频](test-results/install-smoke-20261007/install-smoke/video.mp4) 和 [测试报告](test-results/install-smoke-20261007/report.html)。报告状态为 `complete`；视频为 24 fps、1.625 秒、H.264，音频为 32 kHz 双声道 AAC，逐帧解码、帧数、时间戳和非静音检查均通过。首次生成耗时约 9 分钟，其中读取网络存储上的编码器和模型权重占了较长时间。

后续检查可运行 `./freevideo doctor`。安装过程日志为 `install-final.log`，每次运行的详细日志在 `setup-runs/`。
