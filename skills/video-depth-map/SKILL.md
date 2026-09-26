---
name: video-depth-map
description: 将视频转换为近白远黑、弱化人物纹理的相对深度视频，用于白模视频、深度控制视频和 ComfyUI 深度预处理；适用于用户参考图中的灰度空间层次效果，不用于普通黑白调色或人体抠像。
---

# 视频转深度白模

使用 Depth Anything V2 Small 推断相对远近，再将深度映射为近白远黑。人物、道具和场景都参与深度估计。不能用去饱和、高对比、灰阶量化、运动差分填白替代深度推理：黑衣和白衣应按位置而不是衣服亮度呈现灰度。

## 执行

1. 确认输入视频、输出位置；有参考图时先查看。用 ffprobe 获取分辨率、帧率、帧数、时长和音轨。保留原视频，输出使用新路径。
2. 检查 Python 的 torch、transformers、opencv-python、numpy，以及 ffmpeg/ffprobe。选择空闲 GPU，不中断其他推理；单卡机器传 `--device cuda:0`，无 GPU 可用 `cpu`。优先复用已有环境，缺失依赖使用隔离环境。
3. 模型默认在仓库根目录 `ComfyUI/models/depth/Depth-Anything-V2-Small-hf`。缺失时从官方模型仓库下载 config.json、preprocessor_config.json、model.safetensors；不复制权重进 Skill。其他模型位置传 `--model`。
4. 先运行抽帧预览，查看输出旁的 `.preview.jpg`（左原片、右深度图）；检查首、中、尾人物完整性、遮挡、道具边缘和灰度层次。效果正确后去掉 `--preview` 处理整段。

```bash
python3 <skill目录>/scripts/depth_video.py \
  --input /绝对路径/input.mp4 \
  --output /绝对路径/output_depth.mp4 \
  --device cuda:1 --preview
```

脚本按整段12个采样帧的深度百分位确定统一范围，固定增益3.0、gamma 0.7调亮人物，再双边平滑。该映射来自已验收的琵琶曲案例；新场景如人物与地面过度融白，降低增益并重新预览，不把原片亮度混回深度图。逐帧推理及流式编码避免整段驻留显存。音轨直接复制，输出 H.264 MP4 和参数记录 JSON。

## ComfyUI

[界面工作流模板](assets/ComfyUI_视频转深度图.json)和[API模板](assets/深度图_API.json)使用本机已安装的 `LocalDepthVideo` 节点。使用前把 source、destination 替换成当前任务路径，并选择可用 device。模板中的琵琶曲路径只是案例。

本机节点位置：`ComfyUI/custom_nodes/local_depth_video/__init__.py`。通过 `/object_info/LocalDepthVideo` 检查是否加载。该节点目前调用原项目 `AI-Drama/音乐MV/琵琶曲舞蹈/工作流/depth_video.py`；更换项目或迁移机器时应将节点调用改到本 Skill 脚本并保留显式输入输出参数。模板不是独立插件安装包；节点缺失时先使用 Skill 脚本，不声称模板可以直接运行。不为本任务中断正在运行的 ComfyUI 队列。

## 验收与交付

- ffprobe 核对输出帧数、时长、尺寸、帧率和音轨；完整解码确认没有损坏。
- 查看多个时间点及连续动作，检查人物是否缺肢、扇子是否断裂、亮度是否闪烁。统一灰度范围只减少归一化闪烁，不等于时序深度模型。
- 交付视频、预览对比和工作流路径。指出可见边缘误差，不把失败结果描述为合格。
- 这是单目相对深度，不是实测距离或完整三维重建。

官方模型：https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf
