# 《山魈》分镜与 MiniMax H3 视频 Prompt

## 统一技术与连续性锁定

- 真人电影质感、早清中国山寺、冷青灰月色与油灯暖色；不做二维动画、不做游戏 CG。
- 1344×768、24 fps、每镜 10.125 秒（243 帧）；暂不超分。
- 固定空间锚点：书案和油灯在画面左侧，纸窗在左后方，木门在正中，长榻在画面右侧，床榻在右前方；门、窗、书案和床的位置不能移动。
- S01–S02 只出现孙生；S03–S04 出现孙生与山魈；S05–S06 只出现孙生和不露脸家人局部；S07 只出现孙生；S08 不出现人物。
- 所有视频禁止字幕、片内文字、logo、水印；最终字幕另行由实际音轨 ASR 生成。

## 镜头卡

| 镜头 | 起始状态→结束状态 | 主要人物 | 参考资产 | 声音 |
|---|---|---|---|---|
| S01 | 点灯清扫→孙生躺下，山门风声逼近 | 孙生 | 孙生板、书斋空间板、道具板 | 风、灰尘、油灯，无对白 |
| S02 | 月下熟睡→寝门打开，靴声停在门外 | 孙生 | 孙生板、夜间书斋 | 风、门轴、靴声，无对白 |
| S03 | 寝门半开→山魈弯腰入室 | 山魈、孙生 | 双角色板、夜间书斋 | 山魈喉鸣、孙生屏息 |
| S04 | 山魈俯身→短刀刺腹、被褥拖落 | 山魈、孙生 | 双角色板、道具板 | 刀撞石声、拖拽、孙生一句对白 |
| S05 | 孙生伏地→家人破窗持灯发现 | 孙生、家人局部 | 书斋空间板、爪痕特效板 | 脚步、拍门、喘息，无清晰对白 |
| S06 | 晨光验室→门板五道爪痕和被角卡门 | 孙生、家人局部 | 天亮书斋、爪痕板 | 木屑、布料、远钟，无对白 |
| S07 | 孙生背囊离寺→空书斋门上留痕 | 孙生 | 寺外板、书斋板 | 脚步、风、寺钟，无对白 |
| S08 | 空屋静止→被角被风吹动，片尾寓意后期加字卡 | 无人物 | 天亮书斋板、特效板 | 风和木响，无人声、无音乐 |

## Full-reference Prompt 结构

工作流中的每一镜都使用 H3 Full-reference 六段格式：`subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music`。参考标签固定为 `<Picture 1>` 环境、`<Picture 2>` 孙生、`<Picture 3>` 山魈、`<Picture 4>` 道具/特效；只在实际出现的镜头引用对应标签。

### S01

`subject_definitions`: `<Subject 1>` is the fixed Liugou Temple study in `<Picture 1>`; `<Subject 2>` is Sun Sheng in `<Picture 2>` (S1); `<Subject 3>` is the prop set in `<Picture 4>`. `summary`: `[reference generation + audio reference] Establish the abandoned study and return Sun Sheng to the room.` `retention_analysis`: fully preserve the fixed door, paper window, desk, lamp and bed; preserve Sun Sheng's face, gray-blue robe and satchel; preserve the oil lamp and books. `detailed_description`: Realistic live-action period horror. [Shot 1] Dusk wide shot of the abandoned mountain temple and the same study. [Shot 2] At 00:03.000, the camera tracks Sun Sheng entering from frame right, placing his satchel beside the left writing desk, brushing dust from the desk and bed, and lighting the oil lamp. [Shot 3] At 00:07.000, the camera pushes toward the bed as he lies down; a deep wind rolls from the distant gate toward the room, and he opens his eyes before the cut. No readable text, no other people, no creature. `overall_soundscape`: Dry leaves, distant mountain wind, broom bristles, wood floor creaks, oil lamp flutter and one soft bed creak. `non_diegetic_music`: N/A.

### S02

`subject_definitions`: `<Subject 1>` is the fixed night study in `<Picture 1>`; `<Subject 2>` is Sun Sheng `<Picture 2>` (S1). `summary`: `[reference generation + audio reference] Build the unseen approach through sound before revealing the demon.` `retention_analysis`: fully preserve the room anchors and Sun Sheng's appearance; no demon is visible. `detailed_description`: [Shot 1] The same room at moonlit night; Sun Sheng sleeps on the right bed under the coarse quilt. [Shot 2] At 00:03.200, wind pushes the central wooden door open by itself; the paper window shivers while the oil-lamp flame bends toward the doorway. [Shot 3] At 00:06.800, the camera holds on the dark corridor as heavy boots approach, one step at a time. Sun Sheng wakes, reaches under the pillow, and closes his hand around the hidden knife. End with the unseen boots stopping outside the inner sleeping door. No creature, no family, no extra voice. `overall_soundscape`: Layered wind from gate to courtyard to corridor, door hinges, distant loose wood, three heavy boot impacts and Sun Sheng's restrained breathing. `non_diegetic_music`: N/A.

### S03

`subject_definitions`: `<Subject 1>` is the fixed study `<Picture 1>`; `<Subject 2>` is Sun Sheng `<Picture 2>` (S1); `<Subject 3>` is the Shanxiao `<Picture 3>` (S2). `summary`: `[reference generation + audio reference] Reveal the giant Shanxiao entering the locked study.` `retention_analysis`: fully preserve the creature's scale, yellow-brown skin, long teeth and ragged waist cloth; fully preserve the fixed room and Sun Sheng's costume. `detailed_description`: [Shot 1] Start on the closed inner door in the same room. [Shot 2] At 00:02.500, the door opens inward slowly and the Shanxiao bends under the beam, entering from the center doorway; its shoulders nearly touch both sides of the frame. [Shot 3] At 00:06.500, it circles the bed and leans toward the hidden Sun Sheng, its amber eyes catching the oil lamp. The demon opens its huge mouth and produces a nonverbal stone-like throat roar; Sun Sheng remains under the quilt, lips closed, eyes wide. No attack yet, no additional creature or person. `overall_soundscape`: Door wood groans, heavy footfalls, floor vibration, coarse breathing and the Shanxiao's low nonverbal resonance. `non_diegetic_music`: N/A.

### S04

`subject_definitions`: `<Subject 1>` is Sun Sheng `<Picture 2>` (S1); `<Subject 2>` is Shanxiao `<Picture 3>` (S2); `<Subject 3>` is the short knife and quilt in `<Picture 4>`. `summary`: `[reference generation + audio reference] Sun Sheng makes one desperate resistance and is dragged from the bed.` `retention_analysis`: fully preserve both identities, the knife, quilt, door and bed positions. `detailed_description`: [Shot 1] The Shanxiao bends over the bed, one claw hovering above the quilt. Sun Sheng slowly draws the short knife from beneath the pillow. [Shot 2] At 00:03.000, he thrusts once into the demon's abdomen; the blade strikes with a hollow stone impact, with no blood or gore. Sun Sheng (S1), in the same low male voice, shouts exactly: <d>[Chinese] 妖物，退开！</d> [Shot 3] At 00:06.500, the Shanxiao recoils, then grabs the quilt with one enormous hand and drags Sun Sheng off the bed toward the center door. The camera shakes strongly for one beat and ends on the quilt caught at the threshold. `overall_soundscape`: Blade scrape, stone-like impact, quilt fabric tearing, bed wood creaking, heavy dragging steps and Sun Sheng's short cry. `non_diegetic_music`: N/A.

### S05

`subject_definitions`: `<Subject 1>` is Sun Sheng `<Picture 2>` (S1); `<Subject 2>` is the fixed study `<Picture 1>`. `summary`: `[reference generation] The demon has vanished from view; family members discover the injured scholar through the sealed room.` `retention_analysis`: preserve Sun Sheng, room anchors, and the absence of the demon; family members remain partial silhouettes only. `detailed_description`: [Shot 1] Sun Sheng lies on the stone floor by the central door, breathing hard; the Shanxiao is absent. [Shot 2] At 00:03.000, lamps and hurried feet approach outside; hands strike the door, but the door remains shut. [Shot 3] At 00:06.500, a family member's hand and lamp appear through the paper window opening, revealing Sun Sheng's robe and the quilt corner trapped in the door gap. No full family faces, no demon, no clear spoken sentence. `overall_soundscape`: Running footsteps, lamp metal, repeated door knocks, paper tearing and Sun Sheng's breath. No intelligible dialogue. `non_diegetic_music`: N/A.

### S06

`subject_definitions`: `<Subject 1>` is the fixed dawn study `<Picture 1>`; `<Subject 2>` is Sun Sheng `<Picture 2>` (S1); `<Subject 3>` is the claw-mark effect `<Picture 4>`. `summary`: `[reference generation] Dawn makes the supernatural event physically verifiable.` `retention_analysis`: fully preserve the same door, window, bed, desk and lamp positions; transfer the claw-mark effect only onto the central wooden door. `detailed_description`: [Shot 1] Pale dawn enters through the left paper window. Sun Sheng sits weakly on the edge of the right bed while a family member supports his shoulder from off-camera. [Shot 2] At 00:03.500, the camera pans slowly to the central door, revealing five deep claw grooves with splintered wood and the quilt corner wedged in the gap. [Shot 3] At 00:07.000, the camera pushes into the puncture holes; dust falls, but there is no blood, no ghost and no new person. `overall_soundscape`: Morning wind, cloth movement, wood splinters shifting, one distant temple bell and low breathing. `non_diegetic_music`: N/A.

### S07

`subject_definitions`: `<Subject 1>` is Sun Sheng `<Picture 2>` (S1); `<Subject 2>` is the temple exterior from `<Picture 1>`. `summary`: `[reference generation] Sun Sheng leaves before sunrise and the camera returns to the marked empty room.` `retention_analysis`: fully preserve Sun Sheng's costume and satchel; preserve the temple gate, mountain path and the room's fixed door. `detailed_description`: [Shot 1] Gray dawn wide shot of the temple gate. Sun Sheng exits the study from frame left with his satchel, walking fast but unsteady down the mountain path. [Shot 2] At 00:05.000, the camera stays behind as he disappears into mist. [Shot 3] At 00:07.500, hard cut back to the empty study; the oil lamp is extinguished and the five claw marks remain on the door. No other person, no demon. `overall_soundscape`: Uneven footsteps on stone, satchel leather, mountain wind and one distant bell. `non_diegetic_music`: N/A.

### S08

`subject_definitions`: `<Subject 1>` is the empty dawn study from `<Picture 1>`; `<Subject 2>` is the wind-and-claw-mark effect from `<Picture 4>`. `summary`: `[reference generation] Hold on the physical evidence after the characters have gone.` `retention_analysis`: fully preserve the empty room, door, window, bed, desk and claw marks; no characters are retained. `detailed_description`: [Shot 1] Static wide shot of the empty dawn room. The loose quilt corner caught in the central door gap moves slightly in the draft. [Shot 2] At 00:04.500, the camera makes a very slow push toward the five claw marks; dust crosses the light beam. [Shot 3] At 00:08.000, hold on the dark grooves and let the room settle into silence. Do not generate any people, ghost, creature, dialogue, subtitle, title or visible text; the Chinese ending card is added in post-production. `overall_soundscape`: A thin mountain draft, a single wood creak and soft dust movement; no human voice, animal sound or music. `non_diegetic_music`: N/A.
