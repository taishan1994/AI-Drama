# 《生化危机：爆发夜》主题曲 MV 制作报告

## 项目设定

- 音轨：`../生化危机爆发夜_等不到天亮_YuE2.flac`，时长 4:00。
- 歌词来源：`../主题曲歌词_生化危机爆发夜.md`。已建立 61 条逐句字幕：`字幕/等不到天亮_歌词.srt`。字幕时间按该 FLAC 的逐句人声识别结果校准。
- 画面：16 段，每段目标 15 秒，覆盖 4 分钟歌曲。首镜是雪夜厢式车驾驶，其余镜头按歌词与故事节点铺开。
- 画面风格：真人电影感、生存恐怖、雪夜冷蓝灰调、实景式灯光、克制手持运镜。每段用同一位布莱恩概念帧作 I2V 参考，场景资产单独变化，减少人物和服装漂移。
- 生成模型：MiniMax-H3 FL2VA INT8 ConvRot；官方 MiniMax-H3 FL2VA 8-step PDD LoRA；Qwen3-VL 32B INT8 ConvRot 文本编码器；H3 Video VAE FP16；Euler，8 steps，768×432 设置（模型输出 768×448），24 fps，15 秒。生成片段最终统一裁切/缩放、衔接、加歌词和歌曲音轨。
- 风格查阅：用户提供的 B 站中文预告 [BV1e9gx6tE5z](https://www.bilibili.com/video/BV1e9gx6tE5z/)；对应的 Sony Pictures 官方预告可在 [YouTube](https://www.youtube.com/watch?v=mNd1gb19A-c) 查看。尝试用 yt-dlp 拉取时，B 站返回 TLS 错误，YouTube 返回网络不可达；工作区没有取得预告文件，因此没有将原片画格输入生成或剪进成片。
- 素材来源说明：本版为 AI 重演 MV，不是电影预告剪辑。16 段均由本地 MiniMax-H3 根据本项目生成的布莱恩概念帧与场景资产制作，不能视为原片演员或原片画格。待导入电影素材文件夹目前没有影片文件；取得预告 MP4 后，可按歌词将对应原片镜头替换进本版，并以生成镜头补齐空缺。

## 镜头资产与生成提示词

以下每个 workflow JSON 都保存了该镜头完整的 ComfyUI API 工作流、输入资产、设置和提示词。

### scene_01_vehicle

- 图像参考资产：`../AI补镜素材/Bryan_车内雪夜驾驶.png`
- 工作流：`工作流/scene_01_vehicle_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> A continuous live-action film shot in the visual style of the provided Resident Evil movie reference frame. The same young male medical courier Bryan, identical face, messy brown hair, dark winter courier jacket and vest, driving an old delivery van through a silent snowbound city street at night. Start in the passenger-seat two-shot matching the still: Bryan grips the wheel, checks the icy road, then glances toward the white insulated medical case secured on the passenger seat before looking back to the road. Red dashboard light flickers over his anxious face while headlights reveal drifting snow and abandoned cars through the windshield. The camera makes a restrained handheld push toward his profile, then settles on the case and his hand returning to the wheel; do not cut. Cold blue-gray film grade, realistic practical lighting, subtle film grain, natural human movement, grounded survival-horror atmosphere. Keep Bryan, wardrobe, vehicle interior, case design, and night weather consistent. No extra characters, no deformed hands, no text, no logos, no subtitles, no watermark.

### scene_02_memories

- 图像参考资产：`../AI补镜素材/Bryan_未出生孩子线索.png`
- 工作流：`工作流/scene_02_memories_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. Bryan sits in the parked van, glances at a small ultrasound print/photo tucked in the insulated case, then looks back to the storm-dark road. The same courier, face and clothing remain consistent. The red dashboard glow brushes his worried face; slow handheld push-in, cold blue-gray film look, no readable screen text. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_03_crash

- 图像参考资产：`../AI补镜素材/Bryan_山路车祸.png`
- 工作流：`工作流/scene_03_crash_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan steps out of the crashed delivery van on an icy mountain road, retrieves the same white insulated medical case, sweeps a flashlight across the snow, notices a distant motionless shape, then turns toward the dark tree line. Red emergency light flickers through the blizzard. One continuous restrained handheld shot, realistic motion, no graphic injury. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_04_warehouse

- 图像参考资产：`../AI补镜素材/Bryan_仓库防守.png`
- 工作流：`工作流/scene_04_warehouse_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan braces the warehouse fire door while clutching the same medical case. The door rattles under pressure; he backs away, scans the dark warehouse, and slips toward a broken side exit as snow blows in. Keep the face, jacket and case stable, cold practical fluorescent lighting, one continuous shot, no gore. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_05_street_chase

- 图像参考资产：`../AI补镜素材/Bryan_雪夜医疗箱追逃_概念帧.png`
- 工作流：`工作流/scene_05_street_chase_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan runs toward camera through a deserted snowbound Raccoon City street at night, carrying the same white medical case. The camera tracks backward, he glances over his shoulder as distant infected silhouettes descend from rooftops. Snow sweeps across headlights and wet slushy pavement. Preserve face, jacket, case and cold blue-gray film look; continuous handheld chase, no cuts or gore. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_06_tunnel_reach

- 图像参考资产：`../AI补镜素材/Bryan_隧道求救.png`
- 工作流：`工作流/scene_06_tunnel_reach_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan moves cautiously down a narrow concrete tunnel, holding the medical case close and reaching toward a small distant human figure at the bend. A fluorescent light flickers, the figure retreats out of sight, and Bryan turns when a shadow shifts behind him. Keep any other person indistinct and distant; no harm shown, no gore, single continuous shot. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_07_bite_reveal

- 图像参考资产：`../AI补镜素材/Bryan_咬伤检查.png`
- 工作流：`工作流/scene_07_bite_reveal_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. In the abandoned motel bathroom, the same Bryan slowly rolls up his sleeve and sees the bite on his forearm. He freezes, breathes sharply, looks at his reflection, then covers the wound and grabs the medical case. Keep the injury non-graphic, same face and outfit, cold flickering practical light, intimate handheld framing, no text. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_08_rescue_van

- 图像参考资产：`../AI补镜素材/Bryan_救援车.png`
- 工作流：`工作流/scene_08_rescue_van_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. Two adult allies, visible only as shadowed arms and silhouettes, pull the same Bryan into the rear of a rescue van. He keeps the white medical case locked to his chest. The van doors close as snow and distant silhouettes remain outside; the camera stays inside with Bryan, no identifiable ally faces, no gore, restrained live-action film style. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_09_elevator_28

- 图像参考资产：`../AI补镜素材/Bryan_28层电梯.png`
- 工作流：`工作流/scene_09_elevator_28_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. Inside the same scuffed elevator, Bryan holds the medical case, presses the button for floor 28, then notices his wounded arm trembling. The red floor indicator climbs while the camera slowly tightens on his worried face and the case. Preserve his identity and clothing, claustrophobic cold industrial lighting, one uninterrupted shot, no extra people. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_10_voice_message

- 图像参考资产：`../AI补镜素材/Bryan_录制留言.png`
- 工作流：`工作流/scene_10_voice_message_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan records a quiet voice message on his cracked phone in a dim stairwell. He struggles to speak, pauses, swallows, and looks down at the medical case by his feet. Keep the face and costume consistent, intimate close medium shot, weak green emergency light against cold blue-gray shadows, no readable phone text, no other faces. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_11_empty_tunnel

- 图像参考资产：`../AI补镜素材/Bryan_空隧道阴影.png`
- 工作流：`工作流/scene_11_empty_tunnel_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan advances through the empty service tunnel, seen in three-quarter rear view. The camera tracks slowly behind him; a human-shaped shadow slips around the distant corner, fluorescent strips flicker, and Bryan turns to listen while keeping the case close. Quiet suspense, cold gray-blue film grade, no visible attack or injury. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_12_garage_escape

- 图像参考资产：`../AI补镜素材/Bryan_车库逃跑.png`
- 工作流：`工作流/scene_12_garage_escape_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan sprints across the snow-dusted parking garage toward an open exit, carrying the same medical case. Headlights sweep between pillars and distant infected silhouettes emerge behind him. The camera tracks low beside him and keeps the case visible; preserve clothing and face, no cuts, realistic movement, no gore. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_13_lab_arrival

- 图像参考资产：`../AI补镜素材/Bryan_进入实验室.png`
- 工作流：`工作流/scene_13_lab_arrival_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan enters the stark hospital laboratory carrying the white insulated case. He sets it on a stainless bench beneath harsh surgical light, looks at the sealed vial behind glass, and realizes his own hand is shaking. Red emergency reflections pulse faintly; slow controlled push-in, consistent face and outfit, no logos or text. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_14_vial

- 图像参考资产：`../AI补镜素材/Bryan_实验室争夺针剂.png`
- 工作流：`工作流/scene_14_vial_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. In the same hospital laboratory, Bryan reaches for a sealed medicine vial rolling toward the edge of the metal table. He catches it, looks at his wounded arm, then closes his fist around the vial. Keep the case and his face consistent, cold surgical light with restrained red alarm reflections, realistic hands, no gore, continuous shot. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_15_mutation_shadow

- 图像参考资产：`../AI补镜素材/Bryan_变异阴影.png`
- 工作流：`工作流/scene_15_mutation_shadow_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. The same Bryan stands in an empty hospital corridor, still recognizably human. A flickering light makes his shadow on the wall stretch into an unnatural monstrous shape; he turns toward it, frightened, while clutching the case. Suggest mutation through shadow and posture only, no body transformation or gore, same face and clothes, cold blue-gray grade. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

### scene_16_helicopter_rooftop

- 图像参考资产：`../AI补镜素材/Bryan_直升机探照灯.png`
- 工作流：`工作流/scene_16_helicopter_rooftop_I2V_API.json`
- 参数：432p 768x432，15s，8 steps
- Prompt：

> Live-action survival-horror cinematography matching the provided visual reference. On the snow-covered hospital rooftop, the same Bryan clutches the medical case as a rescue helicopter spotlight sweeps across him and the skyline. He takes one unsteady step toward the beam, then looks back into the night. Keep him small against the hard light, preserve identity, outfit and case, drifting snow, unresolved tragic ending, one continuous shot. Natural restrained acting, realistic movement, detailed cold-weather atmosphere, consistent Bryan appearance and medical case, 24 fps, single continuous shot, no text, no subtitles, no logos, no watermark.

## 输出结构与当前状态

- 分段视频：`分段成片/scene_01.mp4` 至 `scene_16.mp4`。
- 字幕：`字幕/等不到天亮_歌词.srt`。
- 完整成片：`等不到天亮_生化危机爆发夜_AI重演MV_1080p.mp4`，时长核验为 240 秒；使用指定 FLAC、逐句歌词字幕和 1080p 输出画布。源镜头为 768×448，1080p 是放大输出。
- 用户提供的 B 站预告链接已记录；因当前服务器无法连接 B 站/YouTube 下载视频，现有成片未含原片镜头。将预告 MP4 放入 `待导入电影素材/` 后，可继续按歌词换入匹配的原片段。
