# MiniMax H3 \- 视频扩写 Prompt 写作全能指南

# 引言

**本文是一份面向开发者的MiniMax H3多模态视频模型 Prompt 扩写指导文档**

**介绍视频扩写 Prompt 的基础写作规则与全能参考模式下的进阶格式规范，为 H3 建立一套结构化的视频扩写方法，把开放、零散、非结构化的用户输入，整理成模型可理解、可执行、可控的多模态视频生成指令。**

MiniMax H3 是新一代开放通用多模态视频模型。相比过去以文生视频、图生视频、首尾帧生成等单点能力为核心的特化任务模型，H3 更强调在统一上下文中理解文字、图片、视频、音频等多种信息，并通过自然语言指令完成更复杂、更开放的视频创作任务。

这意味着，面向 H3 的 Prompt 写作也需要从“描述一个画面”升级为“组织一段视听内容”。一个有效的扩写 Prompt，不只是告诉模型画面要好看，而是要帮助模型理解完整的创作意图：视频的主体是谁，画面从哪里开始，动作如何发展，镜头如何推进，关键帧之间如何连接，参考素材中的哪些信息需要保留，声音如何与画面同步，以及最终视频应呈现怎样的节奏和结果。



\*本文更偏向开发者和专业创作团队使用

\*如果你希望快速了解 H3 的通用使用方法、提示词基础写法和上手建议，可以优先阅读这份用户向文档：

[🐚MiniMax H3 模型 \- 使用手册](https://vrfi1sk8a0.feishu.cn/wiki/FIWjwgL33ipnkekzk30crmKUnIh)



# 一、文生视频/关键帧生视频

## 1\. 任务介绍

- **T2VA**：根据文字构建完整的视听时间线。

- **I2VA**：T2VA 主体 \+ 首帧 instruction \+ 从首帧继续发展的画面路径。

- **FL2VA**：T2VA 主体 \+ 首尾帧 instruction \+ 从首帧到尾帧的连续路径。

- **L2VA**：T2VA 主体 \+ 尾帧 instruction \+ 从合理的前置状态收敛到尾帧的路径。

## 2\. 最终 Prompt 结构

### 2\.1 第一部分是 instruction

**T2VA** 没有图片对齐 instruction，直接从三个主体字段开始。

**I2VA** 固定使用：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

**FL2VA** 固定使用：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

**L2VA** 固定使用：

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

其中，`N` 是最后一个实际镜头的编号；`S.SS` 是视频有效时长，固定保留两位小数。instruction 必须位于最终 Prompt 的第一行，后面空一行再写主体字段。

### 2\.2 第二部分是三个主体字段

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

- **integrated\_multimodal\_description**：沿时间线描述画面、动作、镜头、说话人、台词、演唱和场景内声音。

- **overall\_soundscape**：概括整段视频的环境声、物理动作声和非语言人声。

- **non\_diegetic\_music**：描述角色听不到、只有观众能听到的背景配乐。

## 3\. 如何把关键帧写进多模态描述

### 3\.1 I2VA：从图片开始，再向后发展

`<Picture 1>` 是视频 0\.00 秒的真实首帧，属于 `[Shot 1]`。描述先建立图片中的风格、主体、构图与场景锚点，再写下一步动作。人物身份、服装、颜色、关键物体和空间关系应保持一致。

推荐结构：**首帧锚点 → 动作起点 → 连续变化 → 结果或反应**。

### 3\.2 FL2VA：描述首帧到尾帧之间的路径

Picture 1 是开头，Picture 2 是结尾。主要集中描述：主体如何位移、姿态如何变化、物体如何被操作、构图如何变化，以及场景或光线如何过渡。

FL2VA 通常优先单镜头，让模型连续地从首帧插值到尾帧；只有明确指定多个镜头时才按指定镜头写。尾帧必须由最后一个 `[Shot N]` 在视频结束时到达。

推荐结构：**首帧状态 → 可观察的中间变化 → 差异逐步缩小 → 尾帧状态**。

### 3\.3 L2VA：反推开头，并在结尾落到图片

`<Picture 1>` 是视频最后一帧，属于最后一个 `[Shot N]`，不是天然属于 Shot 1。先根据用户意图和尾帧反推一个合理的早期状态，再描述人物、物体、相机和场景如何逐步接近参考图。

推荐结构：**合理前态 → 明确的动作与变化路径 → 最后一个镜头逐步收敛 → 尾帧落点**。

## 4\. 共用的三个主体段落写法

### 4\.1 多模态描述按时间线展开

`integrated_multimodal_description` 是扩写主体。每条信息都应对应到可以看见或听见的内容：视觉风格、初始构图、主体外观和位置、场景与关键道具、动作及反应、镜头变化、人物语言和同步发生的场景内声音。

`[Shot 1]` 的开头先写整体风格与初始构图。常见风格包括 `Cinematic`、`live-action`、`2D-animated`、`3D CG`、`claymation`、`watercolor` 和 `vintage film`。关键帧任务的风格应从参考图中提取；T2VA 则根据用户文字选择。

```text
[Shot 1] Live-action, cinematic, a medium-wide shot frames...
```

第一镜不写时间戳。

### 4\.2 镜头与切镜

后续镜头使用连续编号，并在开头写递增且位于视频时长范围内的切镜时间：

```text
[Shot 2] At 00:03.500, the camera cuts to...
```

普通切镜可使用 `the camera cuts to`、`the shot cuts to`、`the shot transitions to`、`the shot changes to` 或 `the shot switches to`，一些更加高级的切镜手法也可以灵活表述。

### 4\.3 镜头运动：运镜 \+ 幅度 \+ 速度

一个完整的镜头运动表达由三个维度组成：**运镜类型**决定相机如何运动，**幅度**说明构图变化范围，**速度**说明变化节奏（中等幅度和常速通常省略）。

|维度|可用表达|说明|
|---|---|---|
|运镜<br>|`Zoom In / Zoom Out`|焦距变化，相机机身不移动|
||`Push In / Pull Out`|相机向前 / 向后移动|
||`Pan Left / Pan Right`|相机位置不变，镜头水平转动|
||`Truck Left / Truck Right`|相机水平平移|
||`Tilt Up / Tilt Down`|相机位置不变，镜头垂直转动|
||`Pedestal Up / Pedestal Down`|相机整体升高 / 降低|
||`Arc Shot`|围绕主体弧形移动|
||`Tracking Shot`|跟随运动主体|
||`Static Shot`|机位和镜头均保持静止|
||`Shake Slightly / Shake Strongly`|轻微 / 强烈抖动|
||`POV`|主体主观视角|
||`Roll Clockwise / Roll Counterclockwise`|沿镜头轴顺时针 / 逆时针滚转|
|幅度|`with small amplitude`|小幅度变化|
||`with large amplitude`|大幅度变化|
|速度|`at slow speed`|慢速运动|
||`at fast speed`|快速运动|

运镜应作为自然英文动作写入镜头：

```text
The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.
The camera pans right with large amplitude at fast speed, revealing the open doorway.
The camera holds a static shot as the runner exits the frame.
```

### 4\.4 说话人、台词与歌声

会说话、演唱或发出画外人声的主体使用稳定编号 `(S1)`、`(S2)`、\.\.\.、`(Sn)`。多个已有编号的人同时说或唱时使用组合编号比如`(S1,S2)`。同一说话人跨镜头保持同一编号；没有发声的人物不分配编号。

说话人第一次出现时，根据画面和声音补充稳定身份，例如人物类型、年龄、性别、是否出镜，以及音高、音色、语速或口音。说话人的称呼、编号、动作和说话方式写在 `<d>` 外；`<d>` 内只写语言标签和用户给出的实际语言内容，原词与标点逐字保留，不翻译、不改写。

```text
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
```

画外音使用精确表达 `says in an off-screen voiceover`。每一段画外音 `<d>` 后立即写明画面中对应人物的嘴唇保持闭合：

```text
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```

同一句台词或歌词跨切镜时，在两段连接位置使用 `<scenetrans>`，并明确声音跨切镜连续；视频结束前台词被截断时使用 `<cutoff>`。可使用 `continues seamlessly across the cut`、`continues uninterrupted into the next shot`、`carries over from the previous shot` 或 `remains audible across the transition` 说明跨镜头的连续性。

### 4\.5 画面文字

画面中实际可见的横幅、招牌、标识、字幕或霓虹文字使用英文双引号包围，原文与标点逐字保留，不翻译。

```text
A red neon sign reading "营业中" glows above the doorway.
```

### 4\.6 overall\_soundscape

使用 1–4 句英文，在一个连续段落中概括贯穿整段视频的环境声、物理动作声和非语言人声，例如风雨、交通、脚步、衣料摩擦、碰撞、呼吸、笑声或喘息。对白、演唱和场景内音乐已经写在多模态描述中，不在这里重复。只有用户明确要求整段静音时才写 `N/A`。

```text
overall_soundscape: Steady rain taps against the café windows while low room ambience continues underneath. The entrance bell rings once, followed by wet footsteps and the soft scrape of a chair.
```

### 4\.7 non\_diegetic\_music

使用 1–3 句英文描述角色听不到、只有观众能听到的背景配乐。重点写乐器、速度、节奏和动态变化，不写抽象情绪词或配乐的情感功能。角色能听见的演唱、乐器、广播、电视或手机音乐属于场景内事件，应写入多模态描述。没有画外配乐时写 `N/A`。

```text
non_diegetic_music: Sparse piano notes at a slow tempo, joined by sustained low strings that gradually increase in volume before fading out.
```

## 5\. Cases

### Case 1：T2VA

没有参考图片，直接根据文字构建完整时间线。可以补充与用户意图一致的场景、人物、动作和声音信息。

```text
integrated_multimodal_description: [Shot 1] Cinematic, medium-wide shot. The camera pulls out slowly inside a convenience store illuminated by harsh cool-white fluorescent lights. The glossy white tiled floor reflects the ceiling lights and a trail of rainwater from the glass entrance doors. In the midground, a young on-screen man with wet, shaggy blond hair, wearing a navy windbreaker over a faded grey t-shirt, stands before an open refrigerated display case. He hesitates, lifts a bright green plastic beverage bottle from a metal wire shelf, sets it down, and picks it up again. As he holds the bottle, an off-screen middle-aged man with a calm, deep voice (S1) says, <d>[English] We don't have money.</d> The visible blond man remains silent and keeps his lips closed. [Shot 2] At 00:04.500, the camera cuts to a medium close-up of the blond man and pans right to follow his sudden movement. His face tightens under the stark lighting and his body freezes while his right hand still grips the green bottle from Shot 1. He sharply pushes the bottle back into the empty slot, turns on his heel, lowers his gaze, and walks briskly out of frame to the right.


overall_soundscape: A continuous electrical buzz from the fluorescent lights blends with muffled heavy rain outside. A plastic bottle clatters twice against the metal wire shelf, wet rubber soles squeak on the tiled floor, and rapid footsteps recede down the aisle.


non_diegetic_music: A low, sustained electronic synth drone at a slow tempo, with subtle bass pulses and no swell.
```

### Case 2：I2VA

先写首帧 instruction，再把 Picture 1 中的主体、构图和场景作为 Shot 1 的起点，随后描述画面继续发生的变化。

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, the young woman shown in <Picture 1> remains beside the rain-covered train window, preserving her appearance, clothing, seat position, and the carriage layout. The camera trucks right with small amplitude at slow speed as she lifts her gaze from the folded letter toward the passing city lights. Her reflection moves across the glass while the quiet, breathy young woman (S1) says: <d>[English] I get off at the next station.</d> She folds the letter along its existing crease.

overall_soundscape: The train wheels produce a steady metallic rhythm beneath a low ventilation hum. Rain ticks against the window while paper rustles softly in her hands.

non_diegetic_music: Sustained cello notes at a slow tempo with widely spaced piano tones, gradually decreasing in volume.
```

### Case 3：FL2VA

两张图片分别固定开头与结尾；正文重点不是重复描述两张图，而是补出连接二者的运动路径。以下示例为 8 秒单镜头。

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 8.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a rain-soaked cyclist begins in the position and framing established by Picture 1, holding a closed black umbrella beside a silver bicycle. The camera pulls out with small amplitude at slow speed as she releases the bicycle handle, raises the umbrella above her shoulder, and presses the runner upward until the canopy opens. Water rolls from the expanding fabric while she steps beneath it, rotates the handle into the final angle, and settles into the pose, spacing, and composition established by Picture 2 at the end of the shot.

overall_soundscape: Rain falls steadily on the pavement, followed by the metallic click of the umbrella runner and the soft snap of the canopy opening. Water drips from the bicycle frame as distant traffic passes.

non_diegetic_music: N/A
```

### Case 4：L2VA

图片只固定最后时刻。正文先建立一个兼容的早期状态，再让动作、物体状态和构图在最后一个镜头逐步落到 Picture 1。以下示例为 6 秒单镜头。

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot 1]) aligns with the 6.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a close shot begins with an intact drinking glass near the edge of a dark wooden table, while the same hand and sleeve visible in <Picture 1> approach from the right. The camera pushes in with small amplitude at slow speed as the fingertips strike the rim. The glass tips, falls, and hits the floor with a sharp impact; cracks spread through it as fragments slide outward. Toward the end, the moving pieces lose momentum and settle into the exact broken arrangement, hand position, camera angle, lighting, and final composition established by <Picture 1>.

overall_soundscape: Fingertips tap the glass before it scrapes across the tabletop, falls, and breaks with a sharp crash. Small fragments scatter and gradually stop sliding across the floor.

non_diegetic_music: A low electronic pulse at a slow tempo, ending immediately after the glass breaks.
```





# 二、全能参考

本文说明全能参考模式下扩写结果的组织方式与书写格式。

扩写的六个段落正文统一使用英文；只有 `<d>` 中的台词、歌词以及画面中实际可见的文字保留原始语言。

**描述详细度：**`detailed_description` 应尽量详细、明确，逐镜交代当前构图、主体外观与位置、环境与光线、动作及状态变化、相机运动、当下声音，以及参考内容实际出现或生效的位置，避免只概括剧情或引用关系。

> 镜头、运镜、说话人、台词和普通声音的基础写法与 以上【视频扩写 Prompt 写作指南（T2VA / I2VA / FL2VA / L2VA）】 共用。以下重点说明全能参考模式独有的引用标签、分析段落和格式差异。
> 
> 

## 1\. 整体结构

一份完整扩写结果由六个段落组成，按以下顺序排列：

|段落|作用|
|---|---|
|`subject_definitions`|定义参考内容及其引用标签|
|`summary`|概括任务类型、目标视频和主要引用关系|
|`retention_analysis`|说明参考内容的保留、迁移或复用关系|
|`detailed_description`|按播放顺序描述画面、动作、镜头、声音和台词|
|`overall_soundscape`|概括环境声和物理声音|
|`non_diegetic_music`|描述只有观众能够听到的背景配乐|

## 2\. 引用标签与定义（`subject_definitions`）

Ref 扩写使用四类标签标记参考内容的归属：

|标签|表示的内容|
|---|---|
|`<Subject N>`|从参考素材中抽象出的、可在目标视频中复用或修改的可见内容|
|`<Picture N>`|作为具体目标帧或镜头规划依据的参考图片|
|`<Video N>`|提供剪辑源、续写起点或整段时序结构的参考视频|
|`<Audio N>`|被复制或参考的音频信号|

> 某个引用标签一旦分配给一项内容，在 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description` 和声音段落中始终沿用同一含义。
> 
> 

`subject_definitions` 逐项定义后文需要独立追踪的引用内容，例如一个人物、一处场景、一段源视频结构或一条音频。每项引用内容单独使用一行，说明其标签指代什么、承担什么参考作用，以及需要参考的主要特征；需要明确素材归属时，再写出对应的参考来源。如果 `<Picture N>` 或 `<Video N>` 只用于说明另一项引用内容的素材来源，而不会在后文被单独分析或使用，则只在对应定义中引用，不另起一行。各项引用内容出现在哪些镜头，以及被完整保留、部分保留、迁移或复用的情况，统一写在 `retention_analysis` 中。

### 2\.1 `<Subject N>`

`<Subject N>` 用于可重复引用的可见内容，例如：

- 人物、动物或物体

- 场景、背景或环境

- 服装、道具、界面或视觉特效

- 风格、动作、表情或姿态

它表示目标视频实际要使用的内容单元，而不是原始文件本身。一个主体可以由多份参考素材共同定义，一份参考素材也可以提供多个主体。

```text
<Subject 1> is the young woman in <Picture 1>, with long dark hair, a blue cardigan, and a thin silver necklace.
```

同一主体来自多份素材时，合并来源并说明各素材提供的内容：

```text
<Subject 1> is the woman whose appearance comes from <Picture 1> and whose walking motion comes from <Video 1>.
```

### 2\.2 `<Picture N>`

参考图片本身作为某个镜头的首帧、关键帧、尾帧、编辑后关键帧或构图锚点时，使用独立的 `<Picture N>`：

```text
<Picture 2> is the first frame of [Shot 1], showing a woman seated beside a café window.
```

图片只用于定义人物、场景、服装或风格时，不另外创建独立图片条目，而是在对应 `<Subject N>` 中引用图片来源。

图片作为故事板或镜头规划依据时，写清它对应哪些镜头以及提供什么规划信息：

```text
<Picture 3> is a storyboard reference for [Shot 1] and [Shot 2], defining their viewpoint, subject placement, and shot order.
```

### 2\.3 `<Video N>`

`<Video N>` 只用于整段视频层面的关系，例如：

- 原视频剪辑

- 从原视频结尾继续生成

- 参考原视频的运镜、切镜、节奏或时序结构

```text
<Video 1> is the source video for the target video edit.
```

参考视频中的人物、物体、场景、动作或效果如果作为可见内容被复用，仍归入 `<Subject N>`；`<Video N>` 只作为素材来源或结构来源，不代替主体标签。

### 2\.4 `<Audio N>`

`<Audio N>` 表示独立音频素材，或被启用的参考视频同步音轨。常见用途包括：

- 完整或部分复制音频

- 参考背景音乐风格

- 参考说话人的音色和表达方式

- 使用原音频中的台词、歌词或音效

- 参考节拍、节奏或声音连续性

`<Audio N>` 明确对应某个目标说话人时，在定义中沿用该说话人的全局编号：对应已定义主体时写作 `<Subject N> (Sx)`，否则使用稳定的声音称呼加 `(Sx)`。该编号来自目标视频统一的说话人顺序，不在音频定义中单独分配或重新编号；编号规则见 5\.4 节：

```text
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
```

同一音频承担多个作用时，合并成一个自然句子描述，不拆成额外的小节。

### 2\.5 同一参考视频的画面轨与音频轨

`<Video N>` 与 `<Audio N>` 各自独立编号，序号只表示它们在所属标签类别中的顺序，不表示二者之间的配对关系。因此，同一份参考视频可以同时对应 `<Video 1>` 和 `<Audio 2>`，序号不同不影响它们来自同一份素材。

普通参考视频不会仅因文件带有声音而自动产生 `<Audio N>`。

`<Audio N>` 的定义主要说明音频用途，不要求固定声明它来自哪个 `<Video N>`。只有需要消除素材来源歧义时，才补充同源关系，例如：

```text
<Video 1> is the source video for the target video edit.
<Audio 2> is the synchronized audio track of <Video 1> and is reused in the target video.
```

## 3\. `summary`

这一段用一个简短英文段落概括目标视频及其引用关系。开头使用方括号标记任务类型：

```text
[reference generation] ...
[video editing + reference generation + audio reuse] ...
```

根据参考素材在目标视频中的实际作用选择任务类型：

|任务类型|使用场景|
|---|---|
|`keyframe completion`|图片作为目标视频的首帧、关键帧、尾帧、编辑后关键帧或其他具体帧锚点|
|`reference generation`|图片、视频或音频提供人物、场景、风格、动作、运镜、分镜规划等生成参考，但不直接作为具体帧或待编辑、续写的源视频|
|`video editing`|直接修改一段已有的源视频；仅编辑图片或在静态关键帧之间生成不属于这一类型|
|`video continuation`|从已有源视频继续、延长、恢复或转接出新的内容|
|`audio reuse`|完整或部分复用同一段音频信号|
|`audio reference`|不直接复制音频信号，只参考配乐风格、音色、台词或歌词内容、音效质感、节拍或声音连续性|

同一任务同时满足多个关系时，使用加号组合，且加号前后各保留一个空格，不重复同一类型。例如，从源视频继续生成并以一张图片作为尾帧时，写作 `[video continuation + keyframe completion]`；编辑源视频并保留原音轨时，可写作 `[video editing + audio reuse]`。

素材中存在视频或音频并不自动产生对应类型。参考视频只提供运镜、切镜或节奏时，通常属于 `reference generation`；只有直接编辑或续写该视频时，才使用 `video editing` 或 `video continuation`。

编辑源视频时，如果原音轨继续可听，通常同时使用 `audio reuse`；续写源视频时，如果只延续原音轨的声音特征而不直接复制信号，通常使用 `audio reference`。

摘要使用前文已经定义的 `<Subject N>`、`<Picture N>`、`<Video N>` 和 `<Audio N>`，简要说明重要主体、镜头流程及素材作用，不在这里引入新的引用标签。

视频编辑类摘要在任务类型之后使用以下开头：

```text
The target video is an edited version of <Video 1>.
```

## 4\. `retention_analysis`

这一段逐项说明每项参考内容在目标视频中的保留、迁移、复制或参考关系。每个引用标签使用一行，并沿用 `subject_definitions` 中已经确定的含义。

### 4\.1 可见内容

`<Subject N>`、`<Picture N>` 和 `<Video N>` 使用以下关系标记。这些标记是格式中的固定英文取值：

|关系标记|含义|
|---|---|
|`fully_preserved`|对应参考内容的既定作用被完整保留|
|`partially_preserved`|对应参考内容仍被使用，但已定义的部分特征发生变化或只保留一部分|
|`attribute_transfer`|参考特征被迁移到另一个可独立识别的目标载体|
|`weak_reference`|只保留宽泛的风格、类别、构图或氛围相似性|

主体条目写法：

```text
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
```

图片条目写法：

```text
<Picture 2> ([Shot 1] first frame): fully_preserved - ...
```

视频结构条目写法：

```text
<Video 1> (cut and pacing structure): weak_reference - ...
```

### 4\.2 音频

`<Audio N>` 使用以下关系标记：

|关系标记|含义|
|---|---|
|`fully_copy`|完整源音频作为目标视频的完整最终音轨|
|`partially_copy`|只复制部分时间段或音频层，或者复制后又增加、删除、替换了其他声音|
|`reference`|不直接复制信号，只参考音色、节奏、音乐风格、台词内容或声音质感|
|`weak_reference`|只保留宽泛的类别或氛围相似性|

```text
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track.
```

```text
<Audio 2>: reference - the target speaker follows <Audio 2>'s voice timbre and measured delivery without copying the original signal.
```

关系标记以该标签在 `subject_definitions` 中已经定义的参考作用为判断范围，不把目标视频中新加入的动作、背景或剧情误写成参考损失。

## 5\. `detailed_description`

这是全能参考模式扩写稿的主体，按目标视频播放顺序逐镜描述画面、动作、声音和台词，并在相关位置插入引用标签。

### 5\.1 基础格式

- **基础写法****框架如下：**

    - 正文使用英文；台词、歌词和画面文字保留原始语言。

    - `[Shot 1]` 表示起始镜头，不带时间戳；后续镜头使用 `[Shot N] At MM:SS.mmm, ...` 标记切镜时间。

    - 运镜作为当前镜头中的自然英文描述，包含需要表达的类型、幅度和速度。

    - 发声者使用 `(S1)`、`(S2)` 等稳定编号，台词和歌词写作 `<d>[Language] ...</d>`。

    - 跨镜头台词、结尾截断和声音连续性分别使用 `<scenetrans>`、`<cutoff>` 及对应的连续性描述。

- **运镜词汇、群体发声、画外音、跨镜头台词和画面文字等****相关****规则及示例****如下：**

    - **常用的规范运镜词汇**

    |    类型|    词汇|
    |---|---|
    |    焦距变化|    `Zoom In`、`Zoom Out`|
    |    前后移动|    `Push In`、`Pull Out`|
    |    水平转动|    `Pan Left`、`Pan Right`|
    |    水平平移|    `Truck Left`、`Truck Right`|
    |    垂直转动|    `Tilt Up`、`Tilt Down`|
    |    垂直移动|    `Pedestal Up`、`Pedestal Down`|
    |    环绕与跟随|    `Arc Shot`、`Tracking Shot`|
    |    静止与抖动|    `Static Shot`、`Shake Slightly`、`Shake Strongly`|
    |    特殊视角|    `POV`、`Roll Clockwise`、`Roll Counterclockwise`|

    - **群体发声**

    a\.群体始终统一发声，且没有成员单独说话或演唱时，整个群体作为一个说话人，共用一个编号：

    ```text
    the youth group (S1) chants together, <d>[English] Save the planet! Protect the trees! Keep the oceans clean!</d>
    ```

    b\.多个已有各自编号的说话人临时同时发声时，使用组合编号：

    ```text
    the three youths (S2,S3,S4) respond in unison, <d>[English] Yes! Ready!</d>
    ```

    - **画外音和内心独白**

    画外音、旁白和内心独白同样使用稳定的说话人编号与 `<d>`，并使用 `off-screen` 或 `voice-over` 说明声音位置。声音表达某个画面内人物的想法、但并非由其嘴部发出时，写清声音与该人物的关系；需要消除歧义时，可补充人物嘴部保持静止。纯画外说话人没有可见嘴部，不写闭嘴描述：

    ```text
    an adult male off-screen narrator with a deep, magnetic voice (S1) says, <d>[English] In the quiet embrace of autumn, a tiny squirrel embarked on its daily quest.</d>
    ```

    - **跨镜头台词与画内声音**

    a\.完整台词在切镜前已经结束时，新镜头直接开始：

    ```text
    [Shot 1] ... the team leader (S1) shouts, <d>[English] Ready, team?</d> [Shot 2] At 00:02.500, the camera cuts to the waiting youth group.
    ```

    b\.同一句台词跨越切镜时，前半句结尾和后半句开头分别使用 `<scenetrans>`，并在新镜头中说明声音从上一镜连续过来：

    ```text
    [Shot 1] ... the off-screen narrator (S1) continues, <d>[English] Beneath the rustling leaves, it unearthed a secret,<scenetrans></d> [Shot 2] At 00:04.500, the shot cuts to an extreme close-up of the glowing gear. The audio seamlessly continues from the previous shot. The same off-screen narrator (S1) concludes, <d>[English] <scenetrans>a glimmering relic of an unknown world.</d>
    ```

    c\.可使用的音频连续性表达包括：

    ```text
    The audio from the [source] continues uninterrupted over this visual.
    The audio seamlessly continues from the previous shot.
    The audio from the previous shot continues over the transition.
    ... continues seamlessly over the cut, transitioning from [A] to [B].
    The off-screen [singer / speaker] (Sx) ... continues [her/his] vocal line from the previous shot.
    [action] is heard off-screen, [continuation] from the previous shot.
    ```

    d\.画内演唱、乐器、广播、电视、手机音乐或动作声跨越切镜连续时，同样使用上述音频连续性表达。`<scenetrans>` 只用于同一句台词或同一行歌词在切镜处被分成两段的情况。

    同一句台词或歌词连续跨越两次切镜时，中间镜头中的 `<d>` 同时以 `<scenetrans>` 开头和结尾：

    ```text
    <d>[English] <scenetrans>it unearthed a secret<scenetrans></d>
    ```

    e\.视频结尾截断

    台词因视频结束而未说完时，在最后一句末尾使用 `<cutoff>`：

    ```text
    <d>[English] Save the planet! Protect the trees! Keep the oceans<cutoff></d>
    ```

    `<scenetrans>` 表示同一句台词跨切镜连续，`<cutoff>` 表示台词被整段视频的结束边界截断。

    - **画面文字**

    画面中实际可见的横幅、招牌、标识或霓虹文字使用双引号标出，保留原始语言和原始内容，不进行翻译：

    ```text
    a red neon sign reading "营业中" glows above the doorway
    ```



### 5\.2 全能参考模式的差异

|维度|T2VA|全能参考模式|
|---|---|---|
|主体字段|`integrated_multimodal_description`|`detailed_description`|
|风格开头|写在 `[Shot 1]` 后|在 `[Shot 1]` 前用 1—2 句英文建立全局视觉风格|
|引用信息|不使用全能参考模式的引用标签|在首次出现和实际作用位置插入 `<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>`|
|音频关系|描述目标视频自身声音|在对应的镜头或声音阶段引用 `<Audio N>`，并说明复制或参考关系|

开头示例：

```text
The target video is in a cinematic, literary music-video style with soft lighting and a slightly desaturated color palette.
[Shot 1] The scene opens in a crowded urban street...
[Shot 2] At 00:09.000, the shot cuts to an extreme close-up...
```

生成类任务的 `detailed_description` 通常为 350—500 个英文单词。台词密集型内容以完整容纳台词时间线为先，不机械补足字数；视频编辑类内容则按源视频复杂度展开，不强制套用生成类区间。单镜头并不自动缩短篇幅，多镜头按各镜头的信息量分配细节。

### 5\.3 引用标签在镜头中的写法

重要 `<Subject N>` 第一次清晰出现时，在镜头实际可见范围内描述其参考特征、画面位置和当前动作；后续镜头继续使用同一标签，不重新定义该标签所指的内容。

具体帧锚点使用以下自然表达：

```text
the shot begins from <Picture 1>
the shot's keyframe corresponds to <Picture 2>
the shot ends on <Picture 3>
```

原视频编辑或续写时，在镜头描述中自然引用 `<Video N>` 的源状态、结构或延续关系。音频在某个镜头或时段实际生效时，在相应位置引用 `<Audio N>`。

### 5\.4 说话人、音频来源与台词

说话人编号及 `<d>` 的基础格式沿用 T2VA。参考主体实际开口时，同时保留视觉引用标签和说话人编号：

```text
<Subject 2> (S1) turns toward the woman and says, <d>[English] Last summer, I went to my grandfather's house. He talked about you.</d>
```

`<Subject N>` 表示引用主体，`(Sx)` 表示实际发声者。主体本人发声时写作 `<Subject N> (Sx)`；同一主体在画外发声时仍沿用该写法，并标明 `off-screen`。发声者不对应已定义主体时，使用稳定的声音称呼加 `(Sx)`。

当台词、歌词、口号等人声内容只是直接复用的 BGM 或完整 soundtrack 中的声音片段，且没有人物、角色或旁白实际发出该声音时，使用 `<Audio N>` 作为声音来源，不额外创造 `(Sx)`。如果声音由具体人物、角色、旁白或其他独立发声者实际发出，则仍为该发声者分配并沿用 `(Sx)`：

```text
When <Audio 1> reaches the phrase <d>[English] I'm lonely lonely lonely lonely lonely I'm lonely</d>, <Subject 1> performs the corresponding hand gesture without becoming a separate speaker source.
```

直接复用参考音频中的台词、旁白或歌词，或输入 prompt 明确要求复述这些内容时，`<d>` 内必须使用忠实的原始字词并保留原语言；无法辨认的部分写作 `[unclear]`，不猜测或改写。标点统一使用表达句意所需的基础书面标点，如 `,`、`.`、`?`和 `!`；删除重复波浪号、emoji、项目符号以及重复或装饰性标点。完整的陈述句、疑问句和感叹句分别在 `</d>` 前以 `.`、`?`或 `!` 结束。

仅参考音色、节奏、情绪或表达方式时，不应将参考音频中的原台词带入目标视频。

`(Sx)` 根据目标视频中的实际发声顺序统一分配。`detailed_description` 在每次实际发声位置沿用对应编号；`subject_definitions` 中与目标说话人绑定的 `<Audio N>` 定义也沿用同一个 `(Sx)`，但不独立分配新编号。`retention_analysis` 不写 `(Sx)`。直接复用的 BGM 或完整 soundtrack 中仅作为音轨内容出现的台词、歌词、口号等人声片段使用 `<Audio N>`；由具体人物、角色、旁白或其他独立发声者实际发出的声音使用 `(Sx)`。

## 6\. `overall_soundscape` 与 `non_diegetic_music`

- `overall_soundscape` ：概括整段视频的环境声和物理声音。

台词、演唱以及与具体镜头同步的声音事件仍写在 `detailed_description` 中：

```text
overall_soundscape: Quiet indoor room tone and a low ventilation hum continue throughout the video.
```

*没有环境声时写：*

```text
overall_soundscape: N/A
```

- `non_diegetic_music` ：描述角色听不到、只有观众能够听到的背景配乐，存在配乐时说明乐器、速度和动态变化：

```text
non_diegetic_music: A restrained solo-piano score at a slow tempo, with sustained low cello underneath and no swell.
```

*没有此类配乐时可写：*

```text
non_diegetic_music: N/A
```

使用参考音频时，只在与其实际声音层对应的段落中说明复制或参考关系：环境声和音效写在 `overall_soundscape`，只有观众能听到的配乐写在 `non_diegetic_music`；同一音频同时提供两类内容时，分别写入两段：

```text
overall_soundscape: The copied ambience layer from <Audio 1> continues throughout the target video.
non_diegetic_music: <Audio 2> is directly reused as the complete audience-only score.
```

完整台词和歌词只写在 `detailed_description` 的 `<d>` 中，不在这两个段落中重复。

## 7\. 完整示例

```text
subject_definitions:
<Subject 1> is the coffee-shop environment in <Picture 1>, featuring an exposed brick wall, an orange tufted sofa with patterned pillows, a neon sign, and a wooden coffee table.
<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>, with thick white fur, pointed ears, a dark nose, and a curved tail.
<Subject 3> is the young blonde woman in <Video 1>, with long blonde hair and a light-pink button-down shirt with rolled-up sleeves.
<Subject 4> is the young man in <Video 2>, with short wavy brown hair and a dark-grey hoodie with drawstrings.
<Audio 1> is the voice-timbre reference for <Subject 3> (S1), containing a spoken English vocal layer.

summary:
[reference generation + audio reference] The target video shows <Subject 3> eating a cookie in <Subject 1>. <Subject 4> enters with <Subject 2>, which lunges toward the cookie. The three-shot exchange uses <Audio 1> as the voice-timbre reference for <Subject 3> and ends with a canned audience laugh.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the Samoyed's thick white fur, pointed ears, dark nose, and curved tail are retained.
<Subject 3> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the blonde woman's identity, long hair, and light-pink shirt are retained.
<Subject 4> (appears in [Shot 1], [Shot 2]): fully_preserved - the young man's short wavy brown hair and dark-grey hoodie are retained.
<Audio 1>: reference - its vocal timbre guides the dialogue delivery of <Subject 3> without copying the original signal.

detailed_description:
The target video uses a realistic multi-camera sitcom style with warm indoor lighting.
[Shot 1] A medium shot establishes <Subject 1>, the coffee shop with its exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table. <Subject 3> (S1), the young woman with long blonde hair and a light-pink button-down shirt with rolled-up sleeves, sits on the sofa holding a chocolate-chip cookie. From the left, <Subject 4>, the young man with short wavy brown hair and a dark-grey hoodie with drawstrings, enters holding the leash of <Subject 2>, the thick-furred white Samoyed with pointed ears, a dark nose, and a curved tail. The dog lunges toward the cookie and pulls the leash taut. <Subject 3> (S1) jerks her hand back and, using the clear youthful voice timbre referenced from <Audio 1>, exclaims with light annoyance, <d>[English] Hey! Watch your dog!</d> She closes her lips and guards the cookie while <Subject 4> pulls the dog back.
[Shot 2] At 00:03.000, the shot cuts to a close-up of <Subject 4> (S2), the young man in the dark-grey hoodie from Shot 1, sitting beside <Subject 3> on the sofa and holding <Subject 2> securely in his arms. <Subject 4> (S2) says in a casual young male voice with a playful tone and an easy conversational pace, <d>[English] He just likes cookies more than me.</d> He closes his mouth into an apologetic smile and strokes the dog's thick white fur.
[Shot 3] At 00:05.000, the shot cuts to a close-up of <Subject 3> (S1), the blonde woman in the light-pink shirt from Shot 1. Her annoyance softens as she looks toward the Samoyed. <Subject 3> (S1) replies in the same clear youthful voice referenced from <Audio 1> with an amused cadence, <d>[English] Well, he has good taste at least.</d> She smiles and raises the cookie in a small toast-like gesture. A classic canned audience laugh begins immediately after the line and continues through the final frame.

overall_soundscape:
Soft indoor coffee-shop room tone continues throughout the scene.

non_diegetic_music:
N/A
```



