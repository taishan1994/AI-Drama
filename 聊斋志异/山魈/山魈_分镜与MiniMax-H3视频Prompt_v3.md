# 《山魈》高潮重制版分镜文档 v3

本版按 `AI-Drama/skills/minimax-h3-skills/3d-animation-short-generator/references/storyboard-guidelines.md` 的文字分镜字段组织，并按 `AI-Drama/skills/转场skill/转场skill.md` 选择组间转场。默认使用文字分镜，不先生成铅笔分镜图；每个镜头独立生成、独立验收。

## 项目头信息

- 项目：聊斋志异·山魈
- 模型：MiniMax H3 Ref2VA INT8 ConvRot + ACC 8-step + SageAttention
- 分辨率：1344×768，24fps
- 故事结构：冷开场悬念 → 时间回溯 → 四次逼近 → 空间高潮 → 证据 → 余悸反转
- 镜头验收：首帧、中帧、尾帧；人物数量、门闩状态、人物出入方向、音频人声分别检查

## S01 / 8s — 门闩里的爪

- **Hook type**: suspense / reveal
- **Scene & characters**: scene:柳沟寺书斋 | char:孙生-01, 山魈-02（只露爪）
- **Spatial anchor card**:
  - Fixed landmarks: 书案与油灯左侧；中央木门和门闩正中；床榻右侧；门槛下沿位于画面下三分之一。
  - Character positions: 孙生前景偏左、俯卧朝中央门，左手抠住门槛；山魈只在中央门缝外出现一只前爪，不出现身体或脸。
  - Exited character status: 家人、完整山魈均不在场；山魈身体留在门外不可见。
  - Lighting baseline: 冷月蓝光从门缝和左纸窗进入，滚动油灯提供低位暖光；爪子经过时暖光短暂熄灭。
- **Continuity from previous**: 片头无前镜；以黑场拖拽声直接进入画面。
- **Continuity to next**: 最后一秒黑屏，保留门板抓挠声和低沉风声，以 J 转场带入数小时前的黄昏风声。
- **Double-binding**: [char:孙生-01] [char:山魈-02] [scene:柳沟寺书斋] [hook:suspense]

### Per-panel four-quadrant content

#### 0–1s [BEAT]

- **Pose + Expression**: 黑场结束；孙生的手指先进入画面，死死抠住门槛，指节发白；身体伏在门内侧，只露半张惊恐侧脸。
- **Camera**: 低机位贴地，缓慢向中央门槛 push-in；不摇镜、不改变门的位置。
- **Audio + Anchor**: SFX 被褥拖过石地、孙生急促吸气；anchor: 门槛下沿中心。
- **Performance**: 先听后看；孙生 mouth-closed，眼睛看向门缝。

#### 1–3s [BEAT]

- **Pose + Expression**: 被角从孙生腿侧被拉向门缝；他另一只手摸索短刀但抓空，肩膀被拉低。
- **Camera**: 低机位跟随被角横向移动，保持中央门和门闩在背景正中。
- **Audio + Anchor**: SFX 布料摩擦、石地刮擦、门闩轻震；anchor: 被角由右前景向中央门缝移动。
- **Performance**: 孙生目光从手移到门闩，呼吸加快；[HANDOFF → 3–5s 爪入门缝]

#### 3–5s [BEAT]

- **Pose + Expression**: 一只巨大黄褐色爪子从门缝外伸入，钩住被角后突然收回；孙生向后撑地，嘴张开但不发清晰台词。
- **Camera**: 固定低角度，爪子进入时轻微 handheld-shake 一次；不展示山魈全身。
- **Audio + Anchor**: SFX 低沉喉鸣、木板抓挠；anchor: 爪尖与门缝中心。
- **Performance**: 爪子动作一次完成，不重复；孙生 mouth-open 但只喘息。

#### 5–7s [BEAT]

- **Pose + Expression**: 油灯从左侧滚入，暖光扫过中央木门；五道新鲜爪痕从门内侧出现，孙生盯住门闩，确认门仍然没有打开。
- **Camera**: 从爪痕向上 tilt 到门闩，轻微 rack-focus；门闩始终在画面正中。
- **Audio + Anchor**: SFX 灯壶滚动、木头裂响、低频风声；anchor: 门闩正中，爪痕向上延伸。
- **Performance**: 孙生眼神从恐惧转为不解；不出现血、红液、额外人物。

#### 7–8s [HANDOFF → S02 opening]

- **Pose + Expression**: 孙生抬头看向门外，画面快速压暗至黑；最后一帧只保留未落下的门闩声音。
- **Camera**: 极短 pull-back 后黑屏；不得淡出超过 0.3 秒。
- **Audio + Anchor**: J 转场：门板抓挠声和风声跨黑屏延续到 S02 黄昏；无对白。
- **Performance**: 无新增动作；黑屏用于明确“数小时前”的时间跳跃。

### ASCII layout

```text
[0–3s]      desk + lamp (L)       latched door (C)
             S1 hand/body (front)  quilt → seam
[3–5s]                             claw → seam
[5–7s]      rolling lamp (L)      five marks ↑ latch (C)
[7–8s]      BLACK; J-cut wind and scratching into S02
```

## 组间转场表

| 连接 | 类型 | 叙事理由 |
|---|---|---|
| S01→S02 | 黑屏 + J 转场 | 明确从冷开场结果跳回数小时前，风声保持悬念 |
| S02→S03 | 硬切 + L 声桥 | 同一书斋同一夜，油灯声和风声延续 |
| S03→S04 | 硬切 | 同组内压迫升级，不用装饰性转场 |
| S04→S05 | 门缝遮挡转场 | 黑缝占满画面时切入山魈近景，空间连续 |
| S05→S06 | 视线匹配 | 山魈视线落向被褥，切到被褥自行移动 |
| S06→S07 | 动作匹配 | 孙生抓刀的动作直接接刺腹动作 |
| S07→S08 | 硬切 + 拖拽声桥 | 冲击声后立即进入拖拽，保持动势 |
| S08→S09 | 甩镜头 | 被拖过石地的剧烈情绪跃升，进入喊退高潮 |
| S09→S10 | 黑屏 + 声音桥 | 油灯熄灭后先听见家人奔跑，再破窗见光 |
| S10→S11 | 叠化 | 夜惊到天亮验痕，时间流逝明确 |
| S11→S12 | 形状匹配 | 五道爪痕的竖线匹配山路湿脚印，再切空屋门板 |

## S01 生成验收门槛

必须同时满足：1）门闩全程未落；2）只出现孙生和一只爪，不出现完整山魈、家人或第二个人；3）被角从床/前景向中央门缝移动；4）无血无红色液体；5）尾帧可黑屏并承接 S02 的风声。任一项失败，S01 不进入后续镜头生成。
