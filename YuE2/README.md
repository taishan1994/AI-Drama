# YuE2 安装与 ComfyUI 工作流

本目录收纳 YuE2 的本地安装记录、ComfyUI 工作流和复用说明。当前工作区已经安装并运行过 YuE2；以下步骤也可供新环境参考。

## 工作流

- [YuE2 文生音乐（ComfyUI UI 工作流）](workflows/YuE2_文生音乐.json)：输入歌词与风格描述，先生成 ABC 旋律规划，再生成歌曲。
- [YuE2 音乐翻唱（ComfyUI UI 工作流）](workflows/YuE2_音乐翻唱.json)：加载参考音频并按歌词/风格生成翻唱。依赖 SheetSage2 音频编码器。
- [YuE2 文生音乐（API 示例）](workflows/YuE2_文生音乐_API_示例.json)：ComfyUI `/prompt` API 格式，歌词和风格为占位内容。

前两份是可在 ComfyUI 画布中打开的 UI 工作流；API 示例用于脚本提交，不是画布工作流。工作流来自当前安装的 ComfyUI 官方 YuE2 模板。模型选择器中的文件名需与本机实际安装一致。

## 当前环境安装状态

ComfyUI 根目录：`/nfs/FM/gongoubo/new_project/github/aigc/ComfyUI`

| 用途 | 文件 | ComfyUI 位置 |
|---|---|---|
| 官方 YuE2-3B BF16 权重与配置/tokenizer | `YuE2-3B/model.safetensors` 等 | `models/YuE2/YuE2-3B/` |
| 官方 YuE2 VAE | `YuE2-Vae/model.safetensors` 等 | `models/YuE2/YuE2-Vae/` |
| ComfyUI 推理 checkpoint（INT8 ConvRot） | `yue2_3b_int8_convrot.safetensors` | `models/checkpoints/` |
| 翻唱参考音频编码器 | `sheetsage2_bf16.safetensors` | `models/audio_encoders/` |

YuE2 的 ABC、音乐生成和空音频 latent 节点已由本机 ComfyUI 原生提供，不需要额外安装 YuE2 custom node。翻唱工作流额外依赖 ComfyUI 的音频加载/编码节点以及 SheetSage2 权重。

## 从 ModelScope 下载官方 YuE2 权重

使用 ModelScope 官方仓库：

- [`m-a-p/YuE2-3B`](https://www.modelscope.cn/models/m-a-p/YuE2-3B)
- [`m-a-p/YuE2-Vae`](https://www.modelscope.cn/models/m-a-p/YuE2-Vae)

在 ComfyUI 所在主机执行（先按实际部署修改 `COMFYUI_DIR`）：

```bash
COMFYUI_DIR=/path/to/ComfyUI
python3 -m venv /tmp/modelscope-download-venv
/tmp/modelscope-download-venv/bin/python -m pip install -U modelscope

/tmp/modelscope-download-venv/bin/modelscope download --model m-a-p/YuE2-3B \
  --local_dir "$COMFYUI_DIR/models/YuE2/YuE2-3B"
/tmp/modelscope-download-venv/bin/modelscope download --model m-a-p/YuE2-Vae \
  --local_dir "$COMFYUI_DIR/models/YuE2/YuE2-Vae"
```

下载结束后确认两个目录包含 `model.safetensors`、配置文件和各自 license。不要把大型模型仓库下载到项目的 Git 工作树中。

## 安装 ComfyUI 推理模型

ComfyUI 工作流使用 INT8 ConvRot checkpoint。当前安装文件名是 `yue2_3b_int8_convrot.safetensors`，放置位置为：

```text
ComfyUI/models/checkpoints/yue2_3b_int8_convrot.safetensors
```

当前环境的该 checkpoint 来自 Comfy-Org YuE2 官方 ComfyUI 模型发布；ComfyUI 官方 [YuE2 文生音乐模板](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/audio_yue2_text2music.json) 中记录的下载地址为：

```text
https://huggingface.co/Comfy-Org/YuE2/resolve/main/checkpoints/yue2_3b_int8_convrot.safetensors
```

翻唱工作流还需 `sheetsage2_bf16.safetensors`，放在：

```text
ComfyUI/models/audio_encoders/sheetsage2_bf16.safetensors
```

请从 ComfyUI 官方 YuE2 翻唱工作流所指向的模型来源取得对应权重；不要用 YuE2 主 checkpoint 替代 SheetSage2。

## ComfyUI 启用与检查

1. 确认 ComfyUI 版本含 YuE2 原生节点实现；本机实现位于 `comfy_extras/nodes_yue2.py`，并包含 YuE2 模型和 tokenizer 支持。
2. 将工作流 JSON 放到 ComfyUI 可访问的位置，或在网页画布中使用“打开工作流”载入本目录里的 JSON。
3. 重启 ComfyUI 或刷新前端；在 checkpoint 下拉框选择 `yue2_3b_int8_convrot.safetensors`。
4. 文生音乐先运行短歌词测试。检查 ABC 规划、音频生成、VAE 解码和保存节点是否依次执行。
5. 翻唱工作流额外选择参考音频，并检查 SheetSage2 是否可加载。
6. 用 `ffprobe` 检查导出文件的时长、采样率、声道数和编码；长歌曲可能需要较长采样时间和显存。

## 独立 Python 推理（可选）

ModelScope 下载的 `YuE2-3B` 仓库内带有官方推理 wheel：
`YuE2-3B/yue2_infer-0.1.5-py3-none-any.whl`。推荐使用单独虚拟环境，避免修改 ComfyUI 的 PyTorch/依赖版本：

```bash
python3 -m venv /path/to/yue2-venv
/path/to/yue2-venv/bin/python -m pip install --upgrade pip
/path/to/yue2-venv/bin/python -m pip install huggingface-hub==0.36.2
/path/to/yue2-venv/bin/python -m pip install \
  /path/to/ComfyUI/models/YuE2/YuE2-3B/yue2_infer-0.1.5-py3-none-any.whl
```

独立推理环境与 ComfyUI 工作流是两种运行方式；只用 ComfyUI 生成时不需要安装该 wheel。

## 已知要求与限制

- 当前本机工作流使用 INT8 ConvRot checkpoint；ModelScope BF16 权重是官方基础模型文件，二者用途和路径不同。
- 当前记录中的独立推理参考环境为 Linux、Python 3.10+、支持 BF16 的 NVIDIA GPU；生成较长歌曲需要较多 GPU 显存。具体速度和显存会随模型、时长、采样设置及 ComfyUI 版本变化。
- 当前官方模型仓库标注的许可证为 CC-BY-NC-4.0。商用前请重新核对模型及依赖的许可证。
- `YuE2_音乐翻唱.json` 依赖 SheetSage2；仅使用文生音乐时不需要该编码器。

## 来源与本地记录

- 官方模型仓库：ModelScope `m-a-p/YuE2-3B`、`m-a-p/YuE2-Vae`。
- ComfyUI INT8 checkpoint：Comfy-Org YuE2；下载 URL 见上文。
- 当前项目的实际生成记录：[`短剧/雾锁黑石/音乐/主题曲生成记录_雾锁黑石.md`](../../短剧/雾锁黑石/音乐/主题曲生成记录_雾锁黑石.md)。
- 通用短剧制作流程也引用 API 示例：[short-drama-production-pipeline skill](../skills/short-drama-production-pipeline/SKILL.md)。
