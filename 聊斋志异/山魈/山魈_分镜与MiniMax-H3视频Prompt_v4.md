# 《聊斋志异·山魈：应声》分镜与 MiniMax H3 Ref2VA Prompt v4

【画幅】：16:9 横屏
【模型版本】：MiniMax H3 Ref2VA

## 项目头信息

- **项目**：《聊斋志异·山魈：应声》技能重制版
- **模型/画幅/尺寸**：MiniMax H3 Ref2VA；16:9；沿用项目基线 1344×768，24fps
- **分段**：8 段，时长依次为 7 / 10 / 10 / 10 / 10 / 11 / 15 / 9 秒，总长约 82 秒；单段不超过 15 秒
- **分镜方式**：文字分镜为唯一执行依据；每段按每秒一个画面节拍覆盖完整时长
- **转场方式**：默认硬切；有时间倒叙、空间遮挡或声音先行的段间连接才使用特殊方式，并写明戏剧任务
- **跨段连续性**：每段尾帧明确人物、姿态、道具、门闩、灯火；下一段首帧承接故事状态，同时换景别或机位。段缝参考图仅提供提示词，本文件不直接生成图像。
- **声音锁**：孙生（S1）为同一成年男性普通话声线，低沉略干、语速偏慢、受惊时气息变短；山魈不另造说话声线，只逐字复刻 S1 的已说台词，表演位置以画外音为准。跨段音色如有漂移，保留画面，音频统一时再校准。
- **验收**：每段检查首/中/尾帧、房间左右关系、孙生嘴部与台词归属、声源方向、门闩、灰线与脚印、山魈肢体一致性。

## P1 · 剧本

> 独立剧本文件：`山魈剧本_技能重制_v3.md`。本节内容与该文件同步，分镜看板从本文件编译。

#### 一句话梗概

一个借宿荒寺的书生连答两次敲门声，发现回声已从门外逼到床底；第三次应声会让山魈完整现身，他必须在一只长爪已经伸出床沿时仍不出声，抢在天亮前逃出书斋。

#### 核心悬念与规则

**规则只通过可见变化传达，不由旁白解释：**孙生每回答一次，山魈便越过一个空间阈限：第一次回答后，声音从中央木门移到左侧书案下；第二次回答后，声音移到右侧床榻下；第三次应答会让它从床底完整现身。孙生看见脚印后拒绝再回答。沉默不能让已到床下的爪子消失，却阻止山魈取得最后一次应答、以完整形体进入灯下。观众从声源迁移、灰线脚印和只探出一只爪读懂规则。

山魈不凭空穿过仍上闩的门，不把孙生或被褥拖过门板；它的存在由声源、湿脚印、纸窗上的长臂影子和床底短暂探出的爪子逐步证明。两次应答已让它抵达床下，所以沉默不能阻止长爪袭击；沉默只阻止它完整现身。高潮发生在书斋内，孙生靠闭口、油灯和短刀争取脱身。结尾留下它已学会孙生声音的余悸。

#### 人物与表演锁定

#### 孙生（S1）

二十七岁上下的清瘦成年书生；同一张脸、发髻、灰蓝旧棉袍、深灰腰带、黑布鞋。短刀固定在右手，油灯由左手提拿或放在左侧书案。前段压住惊惧、动作谨慎；第二次回答后眼神开始追踪声源；察觉规则后始终咬紧嘴唇，只以呼吸和眼神表演；高潮中不喊叫。唯一清晰台词为两次低声“谁？”，均来自孙生本人。

#### 山魈（S2）

成年男性体型以上、接近房梁高度；黄褐粗粝皮肤、长臂、黑爪、稀疏长齿，沿用角色设定板。前半段不完整露面，以模仿孙生声音、木器内部的敲击、地上湿脚印和纸窗影子出现；高潮只短暂露出一只爪与前臂，不突然给出多个不同怪物形象。无清晰对白，无动物叫声；声纹为低沉胸腔共振、潮湿呼吸和木面刮擦。

#### 空间与道具连续性

- 固定同一书斋：画面左侧书案与油灯，左后方纸窗，中央木门及内侧门闩，右侧床榻；观众方向始终一致。
- 孙生由中央木门进入；进屋后主要活动范围为中央门至左侧书案、再至右侧床边，不绕房间反复走位。
- 短刀在书案右缘或孙生右手，整片不换手；油灯只在左侧书案与孙生左手之间移动。
- 灰烬只在地面铺一条由门槛方向通向床侧的窄线；S05 湿脚印从床沿下方出现，沿灰线向室内延伸并骤停，门槛前始终没有从门外连续进入的脚印。
- 木门前两次敲声时始终闭合、门闩插在室内；S07 孙生亲手拔闩开门离开。没有任何镜头让关闭的门与穿门动作同时发生。

#### 分场剧本

#### S01｜他自己的声音（冷开场，7 秒）

开场第一帧，孙生背贴右侧床沿，一手捂住嘴，目光锁住中央插闩的木门。孙生自己的声音立即从门的方向传来：“谁？”画面清楚看到孙生没有张口。墙上的灯影里，孙生的影子仍贴着床沿，另一道长臂影子却从床底慢慢伸向门闩。孙生把手捂得更紧。切黑，回到当晚稍早。

#### S02｜借宿柳沟寺（10 秒）

深夜暴雨中，孙生独自进入荒废书斋。他把书囊放在左侧书案旁，关上中央木门并插好门闩；确认纸窗闭合，再把短刀放到书案右缘、油灯放在左缘。床榻在右侧。孙生听见屋外风雨，坐到床沿脱鞋。画面清楚建立门、案、窗、床四个方位，房中没有其他人。

#### S03｜第一次应声（10 秒）

三下敲门声落在中央木门上。孙生从床沿起身，停在距门两步处，先看门闩，再低声问：“谁？”门外没有回答。间隔一拍，木门外传来同样的“谁？”，音色和孙生完全一致。门闩轻颤但仍插着。孙生退回一步，目光扫向左侧书案。镜头不展示门外任何人；紧接着，敲声从书案下响起，声音已换了位置。

#### S04｜第二次应声（10 秒）

敲击从左侧书案底下继续响起，三下，紧贴木板。孙生定在画面中央偏左，右手没有拿刀，嘴唇迟疑张开，仍低声说：“谁？”这一次，回声却从右侧床榻下面传来，紧贴地面，像有人伏在床底学他说话。孙生立即闭嘴，视线从书案移到床底。门闩仍在画面后方中央，未动。

#### S05｜灰线（10 秒）

孙生不再出声。他从左侧书案取一小撮炉灰，在门槛方向至右侧床边撒出一条窄直线，短刀握在右手，油灯仍留在左侧案上。室内静下来后，床沿下方先出现一个湿脚印，随后沿灰线朝室内逐个延伸，走到离床数步处骤然停止；门槛前没有从门外连续进入的轨迹。孙生意识到那东西已经从床底爬出，压住呼吸，闭紧双唇。

#### S06｜床底第三声（11 秒）

床底传出三下敲击。紧接着，床板下用孙生的声音轻声问：“谁？”孙生眼眶一颤，几乎要回答；他咬住下唇，把声音咽回去。纸窗上映出一个高大长臂身影，但窗外风向与影子动作相反。影子抬手时，床底传来湿重呼吸；影子停住，孙生也停住。孙生缓慢举起右手短刀，左手伸向书案上的油灯。

#### S07｜不出声（15 秒，动作高潮）

床底的黑影猛地攥住垂下的被角，向床下拖。孙生双手抓住床架，右手短刀朝床底木板刺下，刀刃只击中木头，发出沉闷撞击；没有血。长爪从床沿下探出，抓住他的衣袖。孙生没有叫喊，左手把油灯举到床底边缘。暖光扫过湿脚印，脚印停在床边；长爪受光缩回暗处。孙生用短刀割断被角，猛地挣脱，退到中央木门旁；他左手拔开门闩，右手仍握短刀。门外雨势变弱，门缝透入一线冷月光。山魈只发出一次低沉喉鸣，没有露出完整身体。

#### S08｜空屋回声（9 秒）

夜雨暂歇。孙生拉开中央木门，侧身跨出门槛，离开书斋；镜头留在室内，床仍在右、书案仍在左、纸窗完整，油灯还亮着。孙生走远后，门在风中缓慢合上，门闩没有自动落下。空房安静两拍。随后右侧床底传来三声敲击，声音清晰地用孙生的音色问：“谁？”画面中没有人；床底湿脚印停在空床边。切黑。

#### 声音节奏

- 开场先给静音与压抑呼吸，再让孙生自己的声音从错误的位置响起；不要先铺音乐。
- 敲门三组的空间由中央木门 → 左侧书案下 → 右侧床底推进；每次回答后，回声位置更近。
- S05 以后孙生不再说话；嘴唇始终闭合，避免模型自发补台词。
- S07 仅使用床架受力、布料撕裂、刀击木板、油灯轻响、短促呼吸、一次低喉鸣；不加尖叫、旁白或解释规则的对白。
- S08 的最后一句由空房中的模仿声发出；此时画面严格无人、孙生已离画。

#### 本轮重制验收重点

1. 门、案、窗、床的左右关系固定，门闩只在 S07 由孙生主动拔开。
2. 两句“谁？”只能由孙生在 S03、S04 开口；S01 与 S08 的同句是画外模仿声，画面人物嘴唇闭合。
3. 回声声源按门 → 书案下 → 床下推进；湿脚印从床沿下方朝室内延伸，门槛处没有外来脚印，不分叉、不瞬移。
4. 山魈保持同一黄褐色长臂造型；前六段不完整露脸，S07 只给一只爪与前臂。
5. S07 无穿门、穿床、身体瞬移、血液或额外人物；孙生亲手开门离开。
6. S08 房间确实空置，但模仿声仍在，作为结尾反转。


## P2 · 资产清单与固定空间

| 编码 | 名字 | 视图/出图 | @图片N | 用途 |
|---|---|---|---|---|
| CHR-SUNSHENG | 孙生角色设定板 | 四视图 | @图片1 | 脸、发髻、灰蓝棉袍、身形 |
| CHR-SHANXIAO | 山魈角色设定板 | 四视图 | @图片2 | 黄褐粗皮、长臂、黑爪与牙齿 |
| SCN-LIUGOU | 柳沟寺书斋干净空间 | 16:9 环境图 | @图片3 | 左案、后左纸窗、中门、右床固定布局 |
| PROP-STUDY | 书案油灯书囊短刀被褥 | 道具设定板 | @图片4 | 道具外观与初始位置 |
| FX-SHANXIAO | 山魈木屑与爪痕质感 | 特效参考板 | @图片5 | S07 少量干木屑与爪部材质参考 |

固定轴线：画面左侧书案，左后纸窗，中央木门与室内门闩，右侧床榻。全片不镜像翻转环境。孙生进门后，短刀固定右手，油灯固定左手或书案左缘。山魈前六段不完整现身，S07 只显示同一只爪和前臂。

## P2.5 · 资产出图提示词（只提供文字提示，不自动出图）

### KF-S01 · 孙生听见自己的声音
```text
16:9 横屏，真人电影质感，古代柳沟寺书斋。唯一人物孙生背靠画面右侧床沿，左手捂住嘴，眼睛看向中央闭合插闩的木门。画面左侧书案上只有一盏油灯，暖光在后墙投出孙生本人影子之外的一道细长手臂影，影子从床底位置朝中央门闩延伸。严格沿用固定空间布局，单一孙生，表情惊惧克制。
```

### KF-S03 · 第一次应声后书案下有敲击
```text
16:9 横屏，真人电影质感，同一柳沟寺书斋。孙生站在中央木门内两步，门闩插好；他转头看向左侧书案下。书案木腿旁少量木屑轻颤，门、案、纸窗、床位置不变。孙生嘴唇闭合，油灯仍在左案。
```

### KF-S05 · 灰线与湿脚印
```text
16:9 横屏，真人电影质感，固定书斋俯斜视角。地面只有一条窄直炉灰线，从门槛方向通向右侧床前；湿脚印先从床沿下方出现，再沿灰线朝室内延伸，离床数步处骤然停下。门槛前没有从门外进入的连续脚印。孙生蹲在床侧，右手握短刀，嘴唇闭合。无其他人物或实体入画。
```

### KF-S06 · 纸窗上的长臂影
```text
16:9 横屏，真人电影质感，同一固定书斋。孙生站在右床与中央木门之间，右手持短刀、左手刚伸向左案油灯，嘴唇紧闭。左后纸窗映出一条高大长臂影，影子方向与窗外雨风相反；实体山魈不入画。
```

### KF-S07 · 床底长爪
```text
16:9 横屏，真人电影质感，同一固定书斋低机位。右侧床沿下仅伸出一只黄褐色粗粝长爪与短段前臂，抓住孙生灰蓝袍袖；其余身体留在床底阴影。孙生左手提油灯照向爪子，右手握短刀，床边有窄灰线和湿脚印。画面冷月蓝灰与油灯暖光对照。
```

## 段落总览

| 段 | 时长 | Hook | 核心事件 | 段尾状态与下一段开场关系 |
|---|---:|---|---|---|
| S01 他自己的声音 | 7s | 悬念 / 揭示 | 闭嘴的孙生听见自己的声音，影子多出长臂 | 闪回硬切至傍晚，风雨声搭桥；时间变化，重新建立全景 |
| S02 借宿柳沟寺 | 10s | setup | 孙生入室、锁门、建立方位 | 孙生坐床沿，门闩插好、灯在左、刀在案右；S03 切门闩特写 |
| S03 第一次应声 | 10s | suspense | 门外敲门，他回答；同音回声后移至书案下 | 孙生退回门内两步、看向书案；S04 从案下低机位起镜 |
| S04 第二次应声 | 10s | escalation | 书案下敲响；他再答；回声转到床底 | 孙生闭嘴看向床底；S05 俯拍手撒灰 |
| S05 灰线 | 10s | reveal | 湿脚印从床沿下方沿灰线向室内延伸并骤停，门槛前无进入轨迹 | 孙生蹲在床侧，右手刀、左手扶地；S06 从床底低机位切入 |
| S06 床底第三声 | 11s | suspense | 模仿声诱他回答，纸窗单一长臂影横向延展 | 孙生末态在左案旁持灯、右手持刀；S07 硬切至床沿低机位 |
| S07 不出声 | 15s | climax | 山魈抓被角；孙生刺床底、照灯、割被脱身并开门 | 孙生左手握门闩，门开一掌宽、右手持刀；S08 从室内反打门口全景 |
| S08 空屋回声 | 9s | callback / reveal | 孙生离开；空房间用他的声音问“谁？” | 全片结尾，无后续接缝 |

## 段间转场表

| 连接 | 方式 | 画面/声音接缝 | 理由 |
|---|---|---|---|
| S01→S02 | 硬切 + 风雨声桥 | 长臂影子切黑，风雨先入，切到更早的雨夜书斋 | 明确时间倒叙，保留冷开场余悸 |
| S02→S03 | 机位硬切 | 床沿中景切中央门闩近景，门闩与灯火位置不变 | 同一时刻，景别变化建立敲门方向 |
| S03→S04 | 动作/视线匹配切 | 孙生退步的视线切到书案底下敲动的木屑 | 把“声音更近”视觉化，不加装饰转场 |
| S04→S05 | 反应镜头硬切 | 盯床底的面部近景切俯拍地面 | 由惊惧转入主动验证 |
| S05→S06 | 景别跳切 | 床前湿脚印特写切床底低角度 | 声音落点与视觉落点一致 |
| S06→S07 | 换机位硬切 | 左案持灯末态切至右床低机位；孙生转向床沿 | 从诱惑骤入直接攻防 |
| S07→S08 | 门缝遮挡硬切 | 门板由一掌宽打开，下一段反向广角接同一开口与姿态 | 同一连续动作，但更换视角，保住空间关系 |

## P4 · 分镜投喂提示词

### 段1 · S01 / 7s — 他自己的声音

- **H3 API 参数**：`duration_seconds=7`（提示词正文仍按六字段顺序）

- **Hook type**：suspense / reveal
- **Scene & characters**：柳沟寺书斋；孙生（S1）；山魈（S2，仅影子）
- **Spatial anchor card**：门居中且闭合上闩，案与灯在左，床在右；孙生背靠床沿，脸朝门；长臂影子只落在后墙，不出现第二个实体人形。
- **Lighting baseline**：左侧油灯暖光照孙生，门与床底为冷暗区；影子方向与油灯位置明确。
- **Continuity from previous**：开场无前镜；先见孙生压住自己的嘴。
- **Continuity to next**：孙生嘴闭合、背靠床沿，长臂影伸向门闩；黑场后切回早些时候。
- **段缝参考图提示词**：生成 16:9 真人电影感关键帧：柳沟寺书斋固定几何，孙生背靠右侧床沿，左手捂嘴，目光看中央插闩木门；左侧油灯投出第二道长臂影子。只作分镜参考，不直接生成。
- **Double-binding**：[char:孙生-S1] [char:山魈-S2] [scene:柳沟寺书斋] [hook:suspense]

**MiniMax H3 Ref2VA Prompt**

```text
subject_definitions:
<Subject 1> (S1) is Sun Sheng, based on the character reference image in 资产/角色设定板/孙生_角色设定板_真人电影质感_2K.png: a lean adult scholar with the same face, tied hair, gray-blue robe, dark sash, and black cloth shoes.
<Subject 2> is the same Shanxiao from 资产/角色设定板/山魈_角色设定板_真人电影质感_2K.png, shown in this segment only as one elongated long-armed shadow.
<Subject 3> is the fixed Liugou Temple study from 资产/环境设定板/柳沟寺_书斋干净空间_2K.png: desk and oil lamp left, paper window rear-left, latched wooden door center, bed right.
<Subject 4> is the oil lamp and bed from the prop reference; the lamp remains on the left desk.

summary:
[reference generation] Create a 7-second live-action historical horror cold open. Keep the room geometry and Sun Sheng's appearance stable. The visual question is why Sun hears his own voice while his mouth is covered, followed by one impossible shadow.

retention_analysis:
<Subject 1> appears throughout, with lips visibly closed whenever the copied voice is heard.
<Subject 2> appears only as one shadow on the rear wall; no full creature body appears.
<Subject 3> remains fixed in every view: left desk, rear-left paper window, centered latched door, right bed.
<Subject 4> remains on the left desk and supplies the single warm light source.

detailed_description:
[Shot 1] <Subject 1> Sun Sheng is pressed against the right bed, facing the centered closed wooden door. His left palm covers his mouth. A single oil lamp burns on the desk at screen left; its warm light falls across his face while the door and bed underside remain cold and dim. Keep the metal latch visibly inserted on the room side. The camera makes a slow, low push toward his face.
[Shot 2] At 00:02.000, Sun Sheng tightens his hand over his mouth as the copied voice fades. The voice comes from the closed central door; Sun Sheng did not speak.
[Shot 3] At 00:04.000, the camera shifts focus from Sun Sheng's eyes to the rear wall. One elongated shadow with an arm much longer than a human arm slowly extends from the bed-side darkness toward the door latch. The shadow is cast by the oil lamp and does not reveal a body. Sun Sheng rises only halfway while keeping his mouth covered. End on the shadow's fingers near the latch, then cut to black.

overall_soundscape:
Near silence, low rain and wind outside the paper window, one oil-lamp wick crackle, Sun Sheng's restrained breathing, a light wood knock, and one dry scrape from the wall. The copied line is the only intelligible voice; Sun Sheng's mouth stays closed during it.

non_diegetic_music:
No music.
```

### Per-panel four-quadrant content

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–1s | 黑场结束，孙生背靠右床沿，左手迅速捂住嘴 | 近景，床侧低机位，短推 | 油灯芯声；孙生右侧，门中央 | 嘴闭合，眼睛定在门闩 |
| 1–2s | 孙生屏息，肩膀绷紧 | 保持近景，轻微前推 | 安静中一声木门轻响；门中央 | 不说话 |
| 2–3s | 孙生不张口，盯住中央门 | 切孙生面部特写 | 模仿声尾韵来自中央门；嘴部清晰可见 | 孙生 lips closed |
| 3–4s | 孙生捂嘴的手加力，眼睛越过镜头看后墙 | 焦点由眼睛转向背景 | 心跳式低频一次；灯在左 | 画外声结束 |
| 4–5s | 墙上的第二道长臂影从床下方向门闩伸展 | 过肩中近景，缓慢摇向墙 | 布料摩擦、木墙轻刮；影子位于门右侧墙面 | 不出现实体山魈 |
| 5–6s | 孙生沿墙影慢慢站起半身，仍捂嘴 | 低机位略仰 | 呼吸压在掌心里；床右、门中 | 动作克制 |
| 6–7s | 影子指尖抵近门闩，画面切黑 | 固定构图，硬切黑 | 一次短促敲木声，风雨声先入下一段 | [HANDOFF → S02 opening] |

[0-1秒] [镜头1] 黑场结束，孙生背靠右床沿，左手迅速捂住嘴；近景，床侧低机位，短推；油灯芯声；孙生右侧，门中央
[1-2秒] [镜头2] 孙生屏息，肩膀绷紧；保持近景，轻微前推；安静中一声木门轻响；门中央
[2-3秒] [镜头3] 孙生不张口，盯住中央门；切孙生面部特写；模仿声尾韵来自中央门；嘴部清晰可见
[3-4秒] [镜头4] 孙生捂嘴的手加力，眼睛越过镜头看后墙；焦点由眼睛转向背景；心跳式低频一次；灯在左
[4-5秒] [镜头5] 墙上的第二道长臂影从床下方向门闩伸展；过肩中近景，缓慢摇向墙；布料摩擦、木墙轻刮；影子位于门右侧墙面
[5-6秒] [镜头6] 孙生沿墙影慢慢站起半身，仍捂嘴；低机位略仰；呼吸压在掌心里；床右、门中
[6-7秒] [镜头7] 影子指尖抵近门闩，画面切黑；固定构图，硬切黑；一次短促敲木声，风雨声先入下一段



### 段2 · S02 / 10s — 借宿柳沟寺

- **H3 API 参数**：`duration_seconds=10`（提示词正文仍按六字段顺序）

- **Hook type**：setup
- **Scene & characters**：柳沟寺书斋；孙生（S1）
- **Spatial anchor card**：同一固定空间；孙生从中央门进，书囊放左案旁，床在右；门闩由孙生亲手插入。
- **Lighting baseline**：雨夜冷蓝环境光从纸窗进入；油灯在左案提供唯一暖色实光。
- **Continuity from S01**：冷开场影子切回数小时前；雨风声延续，画面回到孙生刚进书斋。
- **Continuity to next**：孙生坐右床沿，门闭且插闩，油灯左、短刀案右；S03 切门闩近景。
- **段缝参考图提示词**：沿用 `S02_回到柳沟寺_清洁构图_2K.png` 的书斋几何，孙生坐床沿、门闭插闩、灯在左案、刀在案右；用于 S03 的开场构图参考。
- **Double-binding**：[char:孙生-S1] [scene:柳沟寺书斋] [hook:setup]

**MiniMax H3 Ref2VA Prompt**

```text
subject_definitions:
<Subject 1> (S1) is Sun Sheng, matching the same face, tied hair, gray-blue robe, dark sash, and black cloth shoes in the character reference.
<Subject 2> is the empty Liugou Temple study in the clean environment reference: desk left, paper window rear-left, central wooden door and inside latch, bed right.
<Subject 3> is Sun Sheng's cloth book satchel, short knife, oil lamp, and simple bed from the project prop reference.

summary:
[reference generation] Create a 10-second historical horror setup in one abandoned temple study on a rainy night. Establish the exact room layout and the scholar's deliberate locking of the central door.

retention_analysis:
<Subject 1> is the only person, entering through the central door and remaining in the same robe and hairstyle.
<Subject 2> stays geometrically fixed for the full segment.
<Subject 3> is placed once: satchel on the floor beside the left desk, knife on the desk's right edge, oil lamp on its left edge.

detailed_description:
[Shot 1] <Subject 1> Sun Sheng enters alone through the centered doorway with rain on his shoulders as the camera holds a wide oblique view from inside the study. The left desk, rear-left paper window, central door, and right bed remain readable around him. He sets his cloth satchel beside the left desk, then turns back. Rain taps outside.
[Shot 2] At 00:04.000, Sun Sheng closes the central wooden door and visibly slides the interior metal latch into place. The door stays shut after this action. [Shot 3] At 00:05.000, he puts his short knife on the desk's right edge and the lit oil lamp on its left edge. Keep the knife and lamp separate and visible.
[Shot 4] At 00:07.000, Sun Sheng sits on the right bed, removes one wet shoe, and looks toward the latched door. His face is tired but alert; his lips remain closed. End with Sun seated on the bed, the door latched, lamp left, knife on the desk's right edge. No other person, creature, moving shadow, or supernatural effect appears yet.

overall_soundscape:
Steady rain outside the rear-left paper window, a mild mountain wind, one door creak, a clear metal latch click, cloth satchel settling on the floor, knife and lamp touching wood, and one quiet bed creak. No intelligible speech.

non_diegetic_music:
No music.
```

### Per-panel four-quadrant content

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–1s | 雨滴打在纸窗外，室内空景建立案左、门中、床右 | 广角，门内斜角，缓慢横移 | 风雨声由左后窗进入 | 无人声 |
| 1–2s | 孙生从中央门进入，肩头有雨水 | 中景，门内斜角，随步轻跟 | 门轴声；孙生由中央门进 | 唯一人物入画 |
| 2–3s | 他把书囊放到书案左侧地面 | 中景保持，微摇向左 | 布囊落地声；书案左 | 不移动其他家具 |
| 3–4s | 孙生回身关中央门 | 中近景，过肩看门 | 门板合拢声；门中央 | 右手关门 |
| 4–5s | 他从室内插上门闩 | 门闩特写，固定 | 金属闩落槽声 | 插闩动作完整可见 |
| 5–6s | 孙生回到左案，把短刀放在案右缘、灯放案左缘 | 中景，斜角轻推 | 刀鞘触木、灯芯声 | 刀灯分置明确 |
| 6–7s | 他看向右侧床榻和纸窗 | 中近景，视线匹配切床与窗 | 雨声渐密 | 表情疲惫警惕 |
| 7–8s | 孙生走到床边坐下，脱下一只湿鞋 | 中景，床侧平视 | 鞋底轻响，床板吱声 | 刀仍在左案右缘 |
| 8–9s | 他抬眼看中央门，手停在膝上 | 近景，缓慢推近 | 风声短暂压低 | 嘴闭合 |
| 9–10s | 镜头停在门闩与孙生同框的位置 | 中景，固定 | 三下敲门声从下一段接入 | [HANDOFF → S03 opening] |

[0-1秒] [镜头1] 雨滴打在纸窗外，室内空景建立案左、门中、床右；广角，门内斜角，缓慢横移；风雨声由左后窗进入
[1-2秒] [镜头2] 孙生从中央门进入，肩头有雨水；中景，门内斜角，随步轻跟；门轴声；孙生由中央门进
[2-3秒] [镜头3] 他把书囊放到书案左侧地面；中景保持，微摇向左；布囊落地声；书案左
[3-4秒] [镜头4] 孙生回身关中央门；中近景，过肩看门；门板合拢声；门中央
[4-5秒] [镜头5] 他从室内插上门闩；门闩特写，固定；金属闩落槽声
[5-6秒] [镜头6] 孙生回到左案，把短刀放在案右缘、灯放案左缘；中景，斜角轻推；刀鞘触木、灯芯声
[6-7秒] [镜头7] 他看向右侧床榻和纸窗；中近景，视线匹配切床与窗；雨声渐密
[7-8秒] [镜头8] 孙生走到床边坐下，脱下一只湿鞋；中景，床侧平视；鞋底轻响，床板吱声
[8-9秒] [镜头9] 他抬眼看中央门，手停在膝上；近景，缓慢推近；风声短暂压低
[9-10秒] [镜头10] 镜头停在门闩与孙生同框的位置；中景，固定；三下敲门声从下一段接入



### 段3 · S03 / 10s — 第一次应声

- **H3 API 参数**：`duration_seconds=10`（提示词正文仍按六字段顺序）

- **Hook type**：suspense
- **Scene & characters**：柳沟寺书斋；孙生（S1）；山魈（S2，门外声音）
- **Spatial anchor card**：孙生由床边走到门内两步处；门仍中间闭合插闩；案与灯左、床右不动。
- **Lighting baseline**：雨夜蓝灰，油灯暖光位于左案。
- **Continuity from S02**：孙生坐床沿，三声敲门引他起身。
- **Continuity to next**：孙生退回门内两步，头转向左案；下一镜从案下低角度开始。
- **段缝参考图提示词**：孙生站在中央门内两步，门闩清晰可见，头转向画面左侧书案；沿用书斋锚点图。
- **Double-binding**：[char:孙生-S1] [char:山魈-S2] [scene:柳沟寺书斋] [hook:suspense]

**MiniMax H3 Ref2VA Prompt**

```text
subject_definitions:
<Subject 1> (S1) is Sun Sheng, the same scholar and costume established in the previous segment.
<Subject 2> is the unseen Shanxiao, using only a copied adult male voice outside the door, then shifting the next three knocks to beneath the left desk; no creature body is visible.
<Subject 3> is the fixed temple study with its centered latched door, left desk and oil lamp, rear-left paper window, and right bed.

summary:
[reference generation] Create a 10-second suspense segment. Sun Sheng answers the unseen caller once; the voice copies his words and moves from the latched central door to beneath the left desk. The room remains physically ordinary and stable.

retention_analysis:
<Subject 1> moves only from the right bed to a position two steps inside the central door, then backs away.
<Subject 2> is first heard copying Sun Sheng outside the closed door, then its next three knocks come from beneath the left desk; it is never shown.
<Subject 3> remains unchanged; the inside latch never moves or opens.

detailed_description:
[Shot 1] <Subject 1> Sun Sheng rises from the right bed and stops two steps inside the central door as the camera begins on the visibly inserted interior latch. Three separate knocks sound outside; the shot cuts from the latch to his cautious face.
[Shot 2] At 00:04.000, Sun Sheng (S1) whispers in a low, careful adult male voice with a 低沉、略干、语速偏慢的声线: <d>[Chinese] 谁？</d>. Show his mouth moving naturally for this line. A short pause follows. [Shot 3] At 00:05.000, the unseen voice beyond the door repeats the exact same words, “谁？”, with the same low timbre and restrained pace. Sun Sheng's lips remain closed during the copied voice.
The latch gives one small metallic tremor but stays inserted. The door remains fully shut; no hand or face appears through it. Sun Sheng backs one step away and turns his gaze toward the left desk. Three knocks now come from beneath that desk, one at a time; a few wood dust particles tremble. End low on the desk underside. Preserve the same lamp position and room layout.

overall_soundscape:
Rain against the rear-left paper window, three dry knocks on the central door, Sun Sheng's single whispered line, an exact copied reply from the other side, one small latch vibration, then a quiet wood tap from the left desk. No footsteps outside and no other voices.

non_diegetic_music:
No music.
```

### Per-panel four-quadrant content

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–1s | 门闩近景，金属闩安静插在木槽里 | 特写，正斜角固定 | 雨声；门居中 | 无人入画 |
| 1–2s | 第一下敲击震动门板，闩仍不动 | 同景别微震 | 一声沉木敲击，声源门外 | 门不打开 |
| 2–3s | 第二、三下敲击；孙生从床边起身入背景 | 中景，门闩前景 | 连续两声敲击；床右有孙生 | 只有一个人物 |
| 3–4s | 孙生停在门内两步，先看门闩 | 中近景，轻推 | 雨声压低 | 嘴闭合，迟疑 |
| 4–5s | 他低声问“谁？” | 面部近景 | 台词来自孙生，门在画外中央 | 嘴部清楚同步 |
| 5–6s | 门外用完全相同的低音回答“谁？” | 门板近景，固定 | 模仿声在门外；室内无人开口 | 闩仍插着 |
| 6–7s | 孙生瞳孔移动，盯住插闩 | 特写 | 金属闩轻颤一声 | 孙生不再说话 |
| 7–8s | 他退一步，右肩转向左侧案 | 中景，跟退半步 | 衣料摩擦 | 不靠近门 |
| 8–9s | 孙生视线转向书案，油灯火焰偏斜 | 中近景，沿视线小摇 | 三下敲击由左案下响起，风从窗后掠过 | 灯仍在案左 |
| 9–10s | 孙生视线落向书案底下，画面切低位 | 低角度切案下 | 木屑随最后一下轻震 | [HANDOFF → S04 opening] |

[0-1秒] [镜头1] 门闩近景，金属闩安静插在木槽里；特写，正斜角固定；雨声；门居中
[1-2秒] [镜头2] 第一下敲击震动门板，闩仍不动；同景别微震；一声沉木敲击，声源门外
[2-3秒] [镜头3] 第二、三下敲击；孙生从床边起身入背景；中景，门闩前景；连续两声敲击；床右有孙生
[3-4秒] [镜头4] 孙生停在门内两步，先看门闩；中近景，轻推；雨声压低
[4-5秒] [镜头5] 他低声问“谁？”；面部近景；台词来自孙生，门在画外中央
[5-6秒] [镜头6] 门外用完全相同的低音回答“谁？”；门板近景，固定；模仿声在门外；室内无人开口
[6-7秒] [镜头7] 孙生瞳孔移动，盯住插闩；特写；金属闩轻颤一声
[7-8秒] [镜头8] 他退一步，右肩转向左侧案；中景，跟退半步；衣料摩擦
[8-9秒] [镜头9] 孙生视线转向书案，油灯火焰偏斜；中近景，沿视线小摇；三下敲击由左案下响起，风从窗后掠过
[9-10秒] [镜头10] 孙生视线落向书案底下，画面切低位；低角度切案下；木屑随最后一下轻震



### 段4 · S04 / 10s — 第二次应声

- **H3 API 参数**：`duration_seconds=10`（提示词正文仍按六字段顺序）

- **Hook type**：suspense / escalation
- **Scene & characters**：柳沟寺书斋；孙生（S1）；山魈（S2，模仿声）
- **Spatial anchor card**：孙生在房间中线偏左；书案前景左、床右、门后景中；声源从书案下跳至床底。
- **Lighting baseline**：左案油灯暖光，床底与地面为冷影。
- **Continuity from S03**：孙生刚转头看书案下，门闩仍闭合。
- **Continuity to next**：孙生站在案与床之间，视线固定床底，嘴闭合；S05 俯拍他取灰。
- **段缝参考图提示词**：房间左侧书案下有轻微木屑震动，孙生站案与床之间，目光看右侧床底，闭口；门闩仍插好。
- **Double-binding**：[char:孙生-S1] [char:山魈-S2] [scene:柳沟寺书斋] [hook:escalation]

**MiniMax H3 Ref2VA Prompt**

```text
subject_definitions:
<Subject 1> (S1) is Sun Sheng, retaining his same face, hairstyle, robe, and body proportions.
<Subject 2> is the unseen Shanxiao, which copies Sun Sheng's exact voice from a new location; after the second answer it has reached beneath the bed, but a third answer would be needed for it to appear fully.
<Subject 3> is the fixed study: left desk, centered latched door, rear-left paper window, right bed.
<Subject 4> is the short knife on the desk's right edge and the oil lamp on its left edge.

summary:
[reference generation] Create a 10-second escalation in which Sun Sheng answers the knocks beneath the left desk and the copied voice relocates beneath the right bed. A third answer would let the Shanxiao fully appear. Keep the source locations visually precise.

retention_analysis:
<Subject 1> stands between the left desk and right bed, then closes his mouth and looks toward the bed underside.
<Subject 2> is heard first beneath the left desk and then beneath the right bed, never as a visible figure.
<Subject 3> stays fixed; central door stays latched.
<Subject 4> does not move or change hands.

detailed_description:
[Shot 1] <Subject 1> Sun Sheng approaches the left desk and stops between it and the right bed while the camera holds floor level beneath the desk. A few wood dust particles tremble with three knocks from inside the desk. Keep the centered door visible in the background with its inside latch inserted.
[Shot 2] At 00:03.000, Sun Sheng (S1) asks softly, with a cautious low male delivery, 低沉、略干、语速偏慢: <d>[Chinese] 谁？</d>. His lips move only for this line. After a short pause, the same voice repeats “谁？” from beneath the right bed. Sun Sheng is visible in the background with his lips closed; he turns his eyes and head toward the bed but does not rush forward. The first answer had moved the voice from the central door to the left desk; this second answer moves it from the desk to the bed.
[Shot 3] At 00:07.000, Sun Sheng presses his lips shut and takes one slow step backward. The camera briefly widens to show desk left, door center, bed right, making the voice's new position legible. End with his gaze fixed on the dark space beneath the bed and one hand reaching toward the left desk. No creature body, no door movement, no extra person.

overall_soundscape:
Three muffled knocks inside the left desk, Sun Sheng's quiet question, a short silence, then the copied question from beneath the right bed. Add restrained rain, shallow breathing, and a small bed-frame creak. No score, no animal calls.

non_diegetic_music:
No music.
```

### Per-panel four-quadrant content

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–1s | 案底木屑轻跳，画面低机位见案腿 | 低角度特写，固定 | 敲击从左案底传来 | 无人物嘴部 |
| 1–2s | 孙生从中央偏后一步步靠近案边 | 中景斜角，轻跟 | 木内三声敲击 | 只孙生一人 |
| 2–3s | 他在案与床中间停住，右手悬在身侧 | 中近景，侧前方 | 雨声降低 | 眼神看案底 |
| 3–4s | 孙生压低声音问“谁？” | 面部近景 | 孙生本人台词 | 嘴部同步，声音克制 |
| 4–5s | 案底静止，没人回答 | 案底特写 | 短暂停顿 | 无动作 |
| 5–6s | 床底传来相同的“谁？” | 切右侧床底低角度 | 模仿声由床底发出 | 孙生在背景不张口 |
| 6–7s | 孙生猛然转眼看床底，身体没有冲过去 | 中近景，快速小摇 | 一声床板轻响 | 不新增对白 |
| 7–8s | 他合紧嘴唇，慢慢后退半步 | 近景，轻拉 | 呼吸变浅 | 嘴闭合 |
| 8–9s | 门闩仍在后方中央，案和床分别在左右 | 广角斜角，短暂重建空间 | 回声尾韵消失 | 位置关系明确 |
| 9–10s | 孙生视线定在床下，手伸向书案 | 中景固定 | 指尖触灰罐声接下一镜 | [HANDOFF → S05 opening] |

[0-1秒] [镜头1] 案底木屑轻跳，画面低机位见案腿；低角度特写，固定；敲击从左案底传来
[1-2秒] [镜头2] 孙生从中央偏后一步步靠近案边；中景斜角，轻跟；木内三声敲击
[2-3秒] [镜头3] 他在案与床中间停住，右手悬在身侧；中近景，侧前方；雨声降低
[3-4秒] [镜头4] 孙生压低声音问“谁？”；面部近景；孙生本人台词
[4-5秒] [镜头5] 案底静止，没人回答；案底特写；短暂停顿
[5-6秒] [镜头6] 床底传来相同的“谁？”；切右侧床底低角度；模仿声由床底发出
[6-7秒] [镜头7] 孙生猛然转眼看床底，身体没有冲过去；中近景，快速小摇；一声床板轻响
[7-8秒] [镜头8] 他合紧嘴唇，慢慢后退半步；近景，轻拉；呼吸变浅
[8-9秒] [镜头9] 门闩仍在后方中央，案和床分别在左右；广角斜角，短暂重建空间；回声尾韵消失
[9-10秒] [镜头10] 孙生视线定在床下，手伸向书案；中景固定；指尖触灰罐声接下一镜



### 段5 · S05 / 10s — 灰线：床下爬出的脚印

- **H3 API 参数**：`duration_seconds=10`（提示词正文仍按六字段顺序）

- **Hook type**：reveal
- **Scene & characters**：柳沟寺书斋；孙生（S1）
- **Spatial anchor card**：门中、案左、床右；孙生由左案取炉灰，在门槛方向至床侧撒出一条直线；湿脚印从床沿下方向室内延伸并骤停。
- **Lighting baseline**：油灯左侧暖光，地面湿脚印在冷暖交界处显形。
- **Continuity from S04**：孙生手伸向书案，眼神仍盯床底。
- **Continuity to next**：孙生蹲在床侧，右手握短刀、左手撑地，嘴闭合；湿脚印从床沿下方延伸至离床数步处后停止。
- **段缝参考图提示词**：俯角看一条窄灰线从门槛方向通向右床；湿脚印从床沿下方出现，沿灰线朝室内走出数步后突然停止，门槛前无外来脚印；孙生蹲在床侧，手持短刀。
- **Double-binding**：[char:孙生-S1] [scene:柳沟寺书斋] [hook:reveal]

**MiniMax H3 Ref2VA Prompt**

```text
subject_definitions:
<Subject 1> (S1) is Sun Sheng, the same silent scholar in the established costume.
<Subject 2> is the fixed Liugou Temple study and its stable left-desk, center-door, right-bed layout.
<Subject 3> is the oil lamp, a small amount of stove ash, and the short knife from the project prop reference.
<Subject 4> is the Shanxiao's supernatural trace: a short line of wet footprints, with no visible feet or body.

summary:
[reference generation] Create a 10-second visual discovery. Sun Sheng silently lays one narrow ash line from the threshold direction toward the bed. Wet footprints emerge from beneath the bed and travel outward into the room, stopping abruptly several steps from the bed; the latched threshold has no continuous incoming trail.

retention_analysis:
<Subject 1> remains the only visible person, silent throughout, crouching beside the right bed by the end.
<Subject 2> preserves the fixed room geometry.
<Subject 3> places the ash on the floor only, keeps the knife in Sun Sheng's right hand, and keeps the lamp on the left desk.
<Subject 4> appears one print at a time, emerging from beneath the right bed and moving outward along the single ash line; the trail stops several steps from the bed, with no continuous prints entering from the latched threshold.

detailed_description:
[Shot 1] <Subject 1> Sun Sheng takes a small amount of ash from the left desk. In a restrained overhead oblique view, he crouches by the central doorway and sprinkles a narrow line from the inside threshold toward the right bed. The door remains closed and latched. He takes the short knife in his right hand and steps back toward the left desk.
[Shot 2] At 00:05.000, the room falls nearly still. One wet footprint appears first just beyond the right bed edge, then three more follow outward along the single ash line into the room. They are adult-sized bare footprints, visibly damp, appearing sequentially without any visible leg, person, or moving cloth. Their direction is unambiguous: from beneath the bed toward the room center. The final print stops several steps from the bed; no track reaches the threshold, branches, or reverses direction.
Sun Sheng remains silent with his lips closed. He crouches near the bed, left hand braced on the floor and short knife held in his right hand, staring at the dark gap beneath the bed. End close to the last wet print. Do not show the monster or make the footprints float.

overall_soundscape:
Rain outside, a small ash container touching wood, ash grains falling onto stone, Sun Sheng's restrained breath, and three soft wet footstep sounds that match the appearance of the prints. No voice and no music.

non_diegetic_music:
No music.
```

### Per-panel four-quadrant content

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–1s | 孙生从左案拿起小撮炉灰 | 手部特写，案左 | 灰罐轻响 | 右手留空 |
| 1–2s | 他蹲到门槛旁，灰落在门内地面 | 俯拍 | 灰粒落石地 | 门闩仍插好 |
| 2–3s | 孙生沿门槛到床边撒一条窄灰线 | 俯角跟拍横移 | 袍摆擦地声 | 不扩成满地灰 |
| 3–4s | 他把短刀握进右手，退到案边 | 中景斜角 | 刀鞘轻响 | 刀固定右手 |
| 4–5s | 空地静止，孙生闭口观察 | 广角固定 | 仅雨声和灯芯声 | 无对白 |
| 5–6s | 床沿下方出现第一个湿脚印 | 地面微距 | 一滴水落地声 | 脚印不带可见腿脚 |
| 6–7s | 后续脚印从床沿向室内依序延伸 | 俯拍跟踪 | 逐次湿印声 | 只沿单线，不到门槛 |
| 7–8s | 脚印在离床数步处骤停 | 地面低机位 | 一次低沉木响 | 不出现完整身体 |
| 8–9s | 孙生蹲下，左手撑地，右手握刀 | 中近景，床侧 | 短促吸气 | 嘴闭合 |
| 9–10s | 他盯住床下，额头微汗，画面落到脚印 | 特写转脚印 | 雨声被压低 | [HANDOFF → S06 opening] |

[0-1秒] [镜头1] 孙生从左案拿起小撮炉灰；手部特写，案左；灰罐轻响
[1-2秒] [镜头2] 他蹲到门槛旁，灰落在门内地面；俯拍；灰粒落石地
[2-3秒] [镜头3] 孙生沿门槛到床边撒一条窄灰线；俯角跟拍横移；袍摆擦地声
[3-4秒] [镜头4] 他把短刀握进右手，退到案边；中景斜角；刀鞘轻响
[4-5秒] [镜头5] 空地静止，孙生闭口观察；广角固定；仅雨声和灯芯声
[5-6秒] [镜头6] 床沿下方显出第一个湿脚印；地面微距；一滴水落地声
[6-7秒] [镜头7] 后续脚印从床沿向室内依序延伸；俯拍跟踪；逐次湿印声
[7-8秒] [镜头8] 脚印在离床数步处骤停，床下保持黑暗；床边低机位；一次低沉木响
[8-9秒] [镜头9] 孙生蹲下，左手撑地，右手握刀；中近景，床侧；短促吸气
[9-10秒] [镜头10] 他盯住床下，额头微汗，画面落到脚印；特写转脚印；雨声被压低



### 段6 · S06 / 11s — 床底第三声

- **H3 API 参数**：`duration_seconds=11`（提示词正文仍按六字段顺序）

- **Hook type**：suspense
- **Scene & characters**：柳沟寺书斋；孙生（S1）；山魈（S2，声音与影子）
- **Spatial anchor card**：开镜孙生蹲在右床前；纸窗左后，影子落窗纸；刀在右手，灯在左案。末态孙生走至左案旁，左手举灯、右手持刀。
- **Lighting baseline**：窗外冷雨光，左案暖灯；影子方向与窗外风向相反。
- **Continuity from S05**：脚印停在床前，孙生低头观察床底。
- **Continuity to next**：孙生末态在左案旁持灯；S07 换机位硬切至右床低角度，孙生左手举灯、右手持刀，立刻转向床边。
- **段缝参考图提示词**：孙生站在左侧书案旁，左手举起油灯、右手短刀垂下；闭口；纸窗出现横向延展的长臂影子，床在画面右侧。
- **Double-binding**：[char:孙生-S1] [char:山魈-S2] [scene:柳沟寺书斋] [hook:suspense]

**MiniMax H3 Ref2VA Prompt**

```text
subject_definitions:
<Subject 1> (S1) is Sun Sheng, the same silent scholar in the gray-blue robe.
<Subject 2> is the same Shanxiao, represented here by Sun Sheng’s copied voice repeating “谁？” and one long-armed shadow on the paper window; no full body appears. The two earlier answers have brought it beneath the bed; a third answer would let it emerge fully.
<Subject 3> is the fixed room with the bed right, latched door center, desk left, and paper window rear-left.
<Subject 4> is the short knife in Sun Sheng's right hand and the oil lamp on the left desk.

summary:
[reference generation] Create an 11-second suspense segment. A third knock and the Shanxiao’s copy of Sun Sheng (S1)’s voice lure him to answer, but he stays silent and sees a shadow that contradicts the wind direction.

retention_analysis:
<Subject 1> crouches by the right bed, then rises and steps to the left desk to lift the lamp; lips stay closed throughout.
<Subject 2> appears only as one window shadow and a nonverbal breath; its copied voice repeats “谁？” but receives no reply.
<Subject 3> remains fixed and the central door remains latched.
<Subject 4> stays consistent: knife in right hand, lamp taken by left hand from the left desk.

detailed_description:
[Shot 1] <Subject 1> Sun Sheng is crouched beside the right bed, tense, as the camera holds floor level on the wet footprints stopping there. Three dull knocks sound beneath the bed. The Shanxiao copies Sun Sheng (S1) in the same low, restrained male timbre (低沉、略干、语速偏慢) and asks from under the bed in Chinese: <d>[Chinese] 谁？</d>. Sun Sheng's lips remain fully closed; he does not answer.
[Shot 2] At 00:04.000, show a close view of his mouth as he nearly responds to the repeated “谁？”, then bites his lower lip and holds silence. The camera shifts to the rear-left paper window. A tall long-armed shadow appears on the paper, moving inward while the rain and wind move outward. It is a flat shadow only, not a second person outside.
Sun Sheng rises slowly between the bed and the door. He takes the short knife in his right hand and lifts the oil lamp with his left. His lips remain closed. End with him beside the left desk, knife down in his right hand, lamp raised in his left, facing the bed and window. Do not show a full demon, extra shadow, or open door.

overall_soundscape:
Three muffled knocks below the bed, the copied voice repeating only “谁？”, restrained breathing, steady rain, one low nonverbal chest resonance, and the small sound of the knife grip and lamp being lifted. No answer from Sun Sheng.

non_diegetic_music:
No music.
```

### Per-panel four-quadrant content

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–1s | 湿脚印停在床边，床底黑暗 | 地面特写，低机位 | 水滴声；床右 | 无声 |
| 1–2s | 床板下传三下敲击 | 床底特写，固定 | 三次闷敲 | 孙生在背景不动 |
| 2–3s | 孙生肩膀一缩，眼睛看床底 | 面部近景，缓推 | 呼吸声 | 嘴闭合 |
| 3–4s | 床底用孙生的低音重复“谁？” | 低角度床沿 | 画外模仿声来自床下 | 孙生不说话 |
| 4–5s | 孙生嘴唇将开未开，咬住下唇 | 嘴与眼特写 | 模仿声尾音 | 不发出应答 |
| 5–6s | 纸窗影子显出高大长臂轮廓 | 切左后纸窗，中景 | 风声方向向外，影子向内移动 | 影子不变成真人 |
| 6–7s | 影子抬起一只长臂，床下发湿重呼吸 | 窗纸与床侧同框，斜角 | 喉腔低鸣一次 | 山魈无台词 |
| 7–8s | 孙生站起半身，嘴唇紧闭 | 中近景，轻仰 | 衣袖摩擦 | 视线盯纸窗影子 |
| 8–9s | 右手拿起短刀，刀尖朝下 | 手部近景 | 刀柄握紧声 | 右手持刀 |
| 9–10s | 左手伸向案左油灯 | 中景，短摇向左 | 灯座轻响 | 刀不换手 |
| 10–11s | 孙生在左侧书案旁持刀与灯 | 中景斜角固定 | 呼吸、雨声 | [HANDOFF → S07 opening] |

[0-1秒] [镜头1] 湿脚印停在床边，床底黑暗；地面特写，低机位；水滴声；床右
[1-2秒] [镜头2] 床板下传三下敲击；床底特写，固定；三次闷敲
[2-3秒] [镜头3] 孙生肩膀一缩，眼睛看床底；面部近景，缓推；呼吸声
[3-4秒] [镜头4] 床底用孙生的低音重复“谁？”；低角度床沿；画外模仿声来自床下
[4-5秒] [镜头5] 孙生嘴唇将开未开，咬住下唇；嘴与眼特写；模仿声尾音
[5-6秒] [镜头6] 纸窗影子显出高大长臂轮廓；切左后纸窗，中景；风声方向向外，影子向内移动
[6-7秒] [镜头7] 影子抬起一只长臂，床下发湿重呼吸；窗纸与床侧同框，斜角；喉腔低鸣一次
[7-8秒] [镜头8] 孙生站起半身，嘴唇紧闭；中近景，轻仰；衣袖摩擦
[8-9秒] [镜头9] 右手拿起短刀，刀尖朝下；手部近景；刀柄握紧声
[9-10秒] [镜头10] 左手伸向案左油灯；中景，短摇向左；灯座轻响
[10-11秒] [镜头11] 孙生在左侧书案旁持刀与灯；中景斜角固定；呼吸、雨声



### 段7 · S07 / 11s — 不出声

- **H3 API 参数**：`duration_seconds=11`
- **Hook type**：climax
- **Scene & characters**：柳沟寺书斋；孙生（S1）；山魈（S2，仅一只爪与前臂）
- **Spatial anchor card**：左案末态硬切到右床低机位；床右、门中、案左。孙生左手持灯、右手持刀；山魈只从床底伸出一只爪抓被角。孙生退到门内拔闩并推开窄缝。
- **Lighting baseline**：室内油灯暖光，窗外冷蓝雨光；暖光照到爪时它缩回。
- **Continuity from S06**：S06 末态在左案旁持灯；S07 换机位硬切至右床边，孙生转身接近床，左右手持物不换。
- **Continuity to next**：孙生亲手拔闩、推门，站在门内侧，左手灯、右手刀；S08 室内反向广角承接他跨门离开。
- **段缝参考图提示词**：孙生站在开了一掌宽的门内，左手油灯、右手短刀垂下，冷雨光进入室内；右床在后景，左案灯仍亮。
- **Double-binding**：[char:孙生-S1] [char:山魈-S2] [scene:柳沟寺书斋] [hook:climax]

**MiniMax H3 Ref2VA Prompt**

```text
Create an 11-second restrained Chinese period horror climax. Preserve the exact room and character from the reference: rainy night, bed right, desk and paper window left, central latched wooden door behind. Hard cut from the previous left-desk shot to a low angle beside the right bed. Sun Sheng moves toward the bed with the oil lamp in his LEFT hand and the short knife lowered in his RIGHT; lips closed, no speech. The quilt edge is abruptly tugged toward the dark gap under the bed. Exactly one long yellow-brown clawed hand with one attached forearm reaches out and catches only the quilt edge. Its body, face and all other limbs stay hidden. The claw never touches Sun Sheng, his clothing, skin or knife; the knife never touches anything. He raises the left-hand lamp; warm light falls on the claw and it releases the quilt and withdraws fully under the bed. Sun Sheng backs to the central door. Close view: his LEFT hand visibly lifts the wooden latch completely out of its socket, then pushes the door narrowly open while keeping the lamp. He stays inside the threshold, right-hand knife down, left-hand lamp raised, cold rain outside. Clean undamaged quilt and dry floor; no blood, red marks, stains, wounds, splinters or debris. Native sound: quick steps, quilt scrape, fabric tug, one tense breath, faint low rumble as the claw withdraws, retreating steps, latch lifted, hinge creak and steady rain. No words, scream, music or narration.
```

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–2s | 孙生从左案硬切到床侧，床沿被角向床底拖动 | 右床低机位，中近景 | 脚步、布料刮地 | 左手灯、右手刀 |
| 2–5s | 一只长爪从床下探出抓住被角 | 床沿近景 | 被角拉紧，压低呼吸 | 只露一爪一前臂，不碰人 |
| 5–7s | 孙生举灯照下，长爪松开并缩回暗处 | 低机位跟灯轻移 | 低喉鸣一次 | 刀始终下垂，不击打 |
| 7–9s | 孙生退向中央门，回头确认床下 | 中景后跟 | 脚步、雨声 | 灯左刀右，房间关系稳定 |
| 9–11s | 左手拔出门闩并推开窄缝，孙生留在门内 | 门闩近景转中景 | 木闩滑动、门轴轻响 | 明确由孙生开门；交接 S08 |

[0–2秒] [镜头1] 左案硬切右床低机位；被角向床底拖动，孙生持灯刀逼近
[2–5秒] [镜头2] 一只长爪伸出只抓被角；不碰人，不见身体
[5–7秒] [镜头3] 左手灯照亮床沿，长爪松开退回；短刀不接触物体
[7–9秒] [镜头4] 孙生持灯刀退向门口，视线仍盯床下
[9–11秒] [镜头5] 左手清晰拔闩并推开门缝；孙生留在门内 [HANDOFF → S08]

### 段8 · S08 / 9s — 空屋回声

- **H3 API 参数**：`duration_seconds=9`（提示词正文仍按六字段顺序）

- **Hook type**：callback / reveal
- **Scene & characters**：柳沟寺书斋；孙生（S1，离开后不在画面）；山魈（S2，仅模仿声）
- **Spatial anchor card**：镜头在室内看中央门，案左、床右、纸窗左后；孙生从门口出画，房内始终无人。
- **Lighting baseline**：冷月光从门口进入，左案油灯仍有微弱火苗。
- **Continuity from S07**：孙生在门内，左手拔闩、右手持刀，门开一掌宽。
- **Continuity to next**：终段；空房中模仿声继续存在，画面切黑。
- **段缝参考图提示词**：书斋室内反打，孙生刚跨出中央门，画面只留其背影离画边缘；房内空无他人，灯在案左，床右，门开一掌宽。
- **Double-binding**：[char:孙生-S1] [char:山魈-S2] [scene:柳沟寺书斋] [hook:callback]

**MiniMax H3 Ref2VA Prompt**

```text
subject_definitions:
<Subject 1> (S1) is Sun Sheng, the same scholar in the gray-blue robe, leaving through the central doorway with the knife in his right hand and oil lamp in his left.
<Subject 2> is the unseen Shanxiao, now able to reproduce Sun Sheng's exact low male voice; it is heard only after he has left.
<Subject 3> is the fixed study: left desk, rear-left paper window, central wooden door and inside latch, right bed.
<Subject 4> is the still-burning oil lamp, the wet footprints, and the ash line left on the floor.

summary:
[reference generation] Create a 9-second final reveal. Sun Sheng leaves the study; the camera stays inside an empty room. After the door closes, the Shanxiao speaks in Sun Sheng's exact voice.

retention_analysis:
<Subject 1> appears only at the beginning, crosses the threshold, and exits frame. He does not return.
<Subject 2> is heard once from beneath the right bed after the room is empty; no visible speaker appears.
<Subject 3> remains fixed and empty. The door closes from the wind but its latch does not engage.
<Subject 4> remains in place: oil lamp on the left desk, ash line and wet prints on the floor.

detailed_description:
[Shot 1] <Subject 1> Sun Sheng stands just inside the central threshold, knife in his right hand and oil lamp in his left, as the camera looks toward him from a reverse oblique angle inside the study. He turns sideways, steps out through the doorway, and exits frame. The camera does not follow him. Preserve the desk on the left, paper window rear-left, door in the center, and bed on the right.
[Shot 2] At 00:03.000, hold on the now-empty room. The oil lamp remains on the left desk; the wet footprints and narrow ash line remain on the floor near the bed. A light breeze slowly swings the door closed. The interior latch stays visibly unengaged; it does not slide by itself.
[Shot 3] At 00:06.000, three dry knocks sound from beneath the right bed. [Shot 4] At 00:07.000, the Shanxiao copies Sun Sheng (S1) in the same low, restrained male timbre (低沉、略干、语速偏慢) and asks in Chinese: <d>[Chinese] 谁？</d>. The camera shows only the empty study; no lips or body are visible. End on the wet footprints stopped beside the right bed, then cut to black.

overall_soundscape:
Sun Sheng's footsteps receding outside, light night wind, the door creaking closed, three dry knocks from beneath the right bed, and one copied line in Sun Sheng's exact low voice. No other speech, no animal sound, no music.

non_diegetic_music:
No music.
```

### Per-panel four-quadrant content

| 时间 | Pose + Expression | Camera | Audio + Anchor | 表演/接续 |
|---|---|---|---|---|
| 0–1s | 从室内反向看门缝，孙生手持刀灯停在门槛 | 广角，室内斜角固定 | 晨风进入 | 状态承接 S07 |
| 1–2s | 孙生侧身跨出中央门 | 中景固定 | 鞋踩门槛声 | 右手刀、左手灯 |
| 2–3s | 孙生背影离画，门保持开一掌宽 | 不跟拍，留室内空间 | 脚步向远处 | 人物退场明确 |
| 3–4s | 空房间全景，门、案、床、窗保持原位 | 广角固定 | 远脚步衰减 | 房间无人 |
| 4–5s | 左案灯火轻晃，刀痕/灰线留在地面 | 缓慢小推 | 灯芯与风声 | 不新增痕迹 |
| 5–6s | 门轻轻合上但门闩未落 | 门侧中景 | 门轴慢响 | 不表现自动上闩 |
| 6–7s | 静止空镜，床底保持黑暗 | 低位固定 | 三声敲击从床底传来 | 无人物入画 |
| 7–8s | 空房内孙生音色问“谁？” | 镜头仍无人 | 山魈模仿孙生 (S1)，声源定位床底 | 无可见说话者 |
| 8–9s | 床下湿脚印停在床边，硬切黑 | 地面近景 | 雨停后的风声，切黑 | [END] |

[0-1秒] [镜头1] 从室内反向看门缝，孙生手持刀灯停在门槛；广角，室内斜角固定；晨风进入
[1-2秒] [镜头2] 孙生侧身跨出中央门；中景固定；鞋踩门槛声
[2-3秒] [镜头3] 孙生背影离画，门保持开一掌宽；不跟拍，留室内空间；脚步向远处
[3-4秒] [镜头4] 空房间全景，门、案、床、窗保持原位；广角固定；远脚步衰减
[4-5秒] [镜头5] 左案灯火轻晃，刀痕/灰线留在地面；缓慢小推；灯芯与风声
[5-6秒] [镜头6] 门轻轻合上但门闩未落；门侧中景；门轴慢响
[6-7秒] [镜头7] 静止空镜，床底保持黑暗；低位固定；三声敲击从床底传来
[7-8秒] [镜头8] 空房内孙生音色问“谁？”；镜头仍无人；山魈模仿孙生 (S1)，声源定位床底
[8-9秒] [镜头9] 床下湿脚印停在床边，硬切黑；地面近景；雨停后的风声，切黑



## 出稿自检

- [x] MiniMax H3 Ref2VA 六段字段顺序固定：`subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music`。
- [x] 每段 7–15 秒；分镜每秒覆盖完整段长。
- [x] 各段首镜都有具名主体锚定；没有开场纯空房镜。
- [x] 全片房间几何、孙生服装、刀手、灯位、门闩状态写明。
- [x] 对白语气位明确，画外模仿声与可见说话人分离；闭口处写明嘴唇闭合。
- [x] 段间逐对写清末态、下段首态、机位变化和叙事接缝。
- [x] 转场只用于时间倒叙、动作/视线匹配、门板遮挡；其他连接硬切。
- [x] 没有将画面正向指令放入负面禁令栏；没有在提示正文中塞入工作流术语。
- [x] 默认只交付文本，不自动生成关键帧或视频。
