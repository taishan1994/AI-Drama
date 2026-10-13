# AI-Drama
抖音：西西嘛呦 对应的AI短剧相关资料

# 使用到的工具

- 花云机场+clash：用于使用codex
- codex：用于生成剧本、分镜，以及生成图片等。
- comfyui+minimax-h3：用于生成视频。
- ffmpeg：用于合成视频以及添加字幕。
- 声纹克隆：fiash-speech、CogVoice3、Qwen3-TTS。
- 语音识别：Whisper large-v3-turbo，用于生成字幕中的文字。
- codex歌词生成+YuE2歌曲编写。

# 一般流程

- screenwriting-skills 设计剧本。
- higgsfield-hell-grind-opensource 设计动作和空间。
- drama-skills 设计分镜和转场。
- higgsfield-hell-grind-opensource 设计资产。声纹使用subject来固定，不额外进行配音。使用codex统一生成资产。
- minimax-writing-skill 重新为分镜写视频生成的prompt。
- codex调用minimax-h3生成分镜视频。

  



