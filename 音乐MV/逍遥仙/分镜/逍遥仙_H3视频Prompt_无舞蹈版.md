# 《逍遥仙》MiniMax-H3 视频 Prompt（无舞蹈参考版）

全片统一：2D hand-painted Chinese ink-and-color animation, refined Shanghai Animation Film Studio inspired visual language, cinematic film grain, expressive brush contours, restrained gouache color blocks, no photorealism, no 3D, no extra characters. All H3 clips are silent; do not generate singing, dialogue, narration, crowd voices, animal sounds, or music. The song is added only after all silent clips pass visual acceptance.

## S00 片头风起纸灯

模式：I2VA，时长 8 秒；引用：`角色设定板_行旅者_v1.png` 仅作风格与主角设计参考，`道具特效设定板_v1.png` 的纸灯和风效参考，S00 首帧关键帧。

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Hand-painted 2D Chinese ink-and-color animation with cinematic film grain. The opening frame shows a dark indigo rice-paper field, one unlit paper lantern fixed near the center, and a thin diagonal ink-wind ribbon entering from the lower left. No people are visible. From 0.00 to 2.00 seconds, the wind ribbon slowly approaches the lantern without moving the lantern's wooden frame. From 2.00 to 4.50 seconds, the lantern wick catches a small warm amber flame; the flame remains small and stable, never enlarging. From 4.50 to 7.00 seconds, the wind carries a few ink leaves across the background and gently reveals a distant blue-gray mountain silhouette. From 7.00 to 8.00 seconds, the camera performs a slow small-amplitude push in toward the lantern, leaving clean negative space above and to the left for the later title card. No subtitles, no logos, no readable text, no character, no singing, no speech.

overall_soundscape: N/A. Generate a completely silent visual clip with no human voice, no animal sound, no footsteps, and no environmental audio.

non_diegetic_music: N/A. Music will be added after visual acceptance.
```

## S01 渡口背影

模式：FL2VA，时长 10 秒；首帧为 S00 尾帧；尾帧为行旅者站在渡口、抬头看远山的关键帧。

```text
How the reference pictures align with the target video — Picture 1 (from [Shot 1]) aligns with the 0.00-second mark of the target video; Picture 2 (from [Shot 2]) aligns with the 10.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Hand-painted 2D Chinese ink-and-color animation. Begin exactly from Picture 1: the same paper lantern, mountain silhouette, wind direction and color palette. The camera pulls out with small amplitude at slow speed as the same lantern stays fixed near center and the old wooden ferry pier gradually appears on the left. From 3.00 to 6.00 seconds, the same protagonist from the character reference enters from the lower right, seen only from behind, wearing the fixed blue-gray robe, cinnabar waist sash and black cloth boots. He walks three measured steps toward the pier; his feet remain connected to the ground and his robe moves only with the left-to-right wind. From 6.00 to 10.00 seconds, he stops at the center-right of the pier and slowly lifts his head toward the distant mountains, reaching the final pose in Picture 2. No other people, no boatman, no text, no subtitles, no speech, no music.

overall_soundscape: N/A. Generate a completely silent visual clip with no footsteps, voices, water sounds, wind sounds, or music.

non_diegetic_music: N/A. Music will be added after visual acceptance.
```

## S02 酒壶与路引

模式：I2VA，时长 8 秒；引用：S01 尾帧、道具特效设定板。

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Begin from the exact S01 ending pose and fixed ferry-pier layout. Cut only to a close-up of the protagonist's right hand and sleeve at the left side of a weathered wine flask and a folded blank travel document resting on the same wooden pier. The hand slowly brushes dust from the document, pauses, then closes the document and moves toward the flask without lifting it. The red cord on the right wrist remains visible. The camera makes a slow small-amplitude push in; no object duplicates or jumps. End with the document closed and the flask still on the pier. No readable writing, no subtitles, no additional people, no speech, no music.

overall_soundscape: N/A. Generate a completely silent visual clip with no paper rustle, no hand sound, no voices, and no music.

non_diegetic_music: N/A. Music will be added after visual acceptance.
```

## 后续镜头执行规范

S03–S14 使用同一角色板、环境板和道具板；每个镜头必须先生成首尾关键帧并检查角色脸、衣服、门/桌/石阶等锚点，再提交 H3。每镜视频只保留一个清晰动作链，不使用随机群演，不让 H3 生成音乐。所有镜头完成后统一挂接 `素材/音频/逍遥仙_筷子兄弟.m4a`，再按最终混音做歌词字幕。
