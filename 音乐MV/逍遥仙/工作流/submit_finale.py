"""Submit the Xuyao Xian finale one accepted shot at a time."""
from pathlib import Path
import json
import sys
import uuid

import requests

ROOT = Path("/data/ssd2/gongoubo/aijuman/音乐mv/逍遥仙")
WF = ROOT / "工作流"
CHECK = ROOT / "检查/动态重制"
API = "http://127.0.0.1:8188"

SHOTS = {
    "R23": ("S11_I2VA_PDD8_api.json", "S11_山河纸鹤_首帧_v1.png", "纸鹤引路"),
    "R24": ("S11_I2VA_PDD8_api.json", "R24_山河长卷_首帧.png", "山河长卷展开"),
    "R25": ("S12_I2VA_PDD8_api.json", "S12_山顶落脚_首帧_v1.png", "山顶站定"),
    "R26": ("S13_I2VA_PDD8_api.json", "R26_回望灯火_首帧.png", "回望人间灯火"),
    "R27": ("S14_I2VA_PDD8_api.json", "S14_山河纸灯收束_首帧_v1.png", "纸灯收束"),
}

PROMPTS = {
    "R23": """中国传统手绘动画，上美影二维手绘质感，纸张纹理、墨线、平涂色块与克制的电影胶片颗粒。严格从提供的山河纸鹤首帧开始，保持同一位行旅者的木簪高髻、长黑发、蓝灰分层长袍、白色破边内层、赭红腰带、黑布靴、右腕红绳和唯一的圆形藤编背包；远山、云海、山路和黄昏冷暖关系固定。固定远景机位，人物在画面中保持原有大小和位置，不推近、不变焦。0到2秒，行旅者沿山路向前缓慢走一步，双脚落地清楚。2到5秒，首帧已有的三只白纸鹤始终留在远处天空上半部，沿左上方向缓慢飞行；每只纸鹤始终小于画面宽度的百分之四，绝不靠近镜头、绝不进入前景、绝不经过人物轮廓前方。5到7秒，人物再走一步，衣摆和红腰带顺同一方向轻摆，云海只缓慢流动。7到8秒，人物停步，纸鹤继续留在远山上空，停在稳定的背影与山河构图。禁止纸鹤放大、近景掠过、遮挡人物、改变形状或数量；禁止变脸、换发型、换衣、复制背包、纸鹤变真人或真鸟、增加人物、日夜突变、字幕和文字。生成纯静音视频，不要生成音乐、对白、旁白、环境声或其他音频。""",
    "R24": """中国传统手绘动画，上美影二维手绘质感，墨线山水、纸张肌理、平涂色块和电影胶片颗粒。严格从R23验收尾帧开始，保持同一片层叠远山、云海和黄昏色调；固定广角机位，人物如在首帧中可见就保持原比例、原位置，不推近、不变焦、不切镜。0到2秒，远处原有纸鹤保持极小的折纸剪影，全部在天空上半部，最大不超过画面宽度百分之三。2到6秒，机位仅做极缓慢的右向横移，近处山脊与远山产生轻微视差，云层缓慢流动，形成水墨长卷展开的感觉；不新增地貌、不改变原有山形。这里是云海山谷，不是海面或江河；画面内绝不出现船、帆、码头或水上交通工具。6到8秒，镜头停在完整辽阔的山河远景，所有纸鹤仍为远处小剪影。禁止任何物体向镜头飞来、禁止前景遮挡、禁止巨型纸片、船只、人物、建筑、动物群、太阳特写、日夜突变、字幕、文字和水印。纯静音视频，不要任何生成音频。""",
    "R25": """中国传统手绘动画，上美影二维手绘质感，纸纹、墨线、平涂色块、电影胶片颗粒。严格从山顶落脚首帧开始，唯一行旅者身份与角色设定板一致：木簪高髻、长黑发、蓝灰分层外袍、白色破边内层、赭红腰带、黑布靴、右腕红绳、一个圆形藤编背包。固定同一山顶岩台、云海与远山，冷蓝与淡金交界的黄昏色温不变。0到2秒，人物从首帧前倾状态缓慢站直，双脚一直踩稳岩面。2到5秒，风吹动发尾、衣摆和腰带，人物只做自然呼吸和微小重心调整，不走出画面、不转身。5到8秒，云海缓慢向远处流动，风势减弱，人物稳定站在山顶中央偏左，镜头只做极轻微后拉并停稳。禁止变脸、发型或服装变化，禁止背包复制、人物漂浮、山体漂移、强光闪变、字幕和文字。纯静音视频，不要任何音频。""",
    "R26": """中国传统手绘动画，上美影二维手绘质感，纸张纹理、墨线、平涂色块与电影胶片颗粒。严格从R25验收尾帧开始，保持相同山顶岩台、远山、云海、人物大小和位置；唯一行旅者保持角色板的高髻长发、蓝灰长袍、白色破边内层、赭红腰带、一个圆形藤编背包和右腕红绳。0到2秒，人物身体和双脚完全不动，只将头部与肩膀缓慢转向左后方回望，动作幅度小而清楚。2到5秒，远处山谷原有的人间灯火由暗至明逐渐亮起，位置固定、数量不增加；云雾轻缓流动。5到7秒，一阵微风掠过，腰带与衣摆轻轻扬起再自然落下。7到8秒，人物维持回望姿势，镜头缓慢后拉少许并稳定。禁止人物走动或转成正面，禁止变脸、换发型、换装、背包变化、灯火爆闪、日出、增加建筑或人物、字幕和文字。纯静音视频，不要任何音频。""",
    "R27": """中国传统手绘动画，上美影二维手绘质感，墨线山水、纸张纹理、平涂色块和克制的电影胶片颗粒。严格从山河纸灯收束首帧开始，保持首帧构图完全固定：深蓝夜空、远山云海、山谷微弱灯火、固定在天空上方中央的一轮圆月，以及画面右侧高杆上的一盏纸灯。月亮从第一帧到最后一帧保持完全相同的位置、直径和亮度；灯杆与纸灯也保持相同位置、尺寸。固定机位，禁止推拉、摇移、变焦或改变视角。0到3秒，只有远处云海作极缓慢的横向流动，月亮和灯杆不动。3到6秒，纸灯芯由暗转暖，出现一粒小而稳定的火光，暖光只映亮灯罩内部边缘。6到8秒，云雾继续轻缓流动，画面停在安静的山河与纸灯构图，留出干净深蓝空间供后期排片名。不要新增或移动任何对象；禁止人物、动物、太阳、第二盏灯、任何文字、字幕和水印。纯静音视频，不要任何音频。""",
}


def main():
    shot = sys.argv[1] if len(sys.argv) > 1 else "R23"
    if shot not in SHOTS:
        raise SystemExit(f"unknown shot: {shot}")
    workflow_name, frame_name, title = SHOTS[shot]
    frame_path = Path("/data/ssd2/gongoubo/aijuman/h3/ComfyUI/input/逍遥仙/关键帧") / frame_name
    if not frame_path.is_file():
        raise SystemExit(f"missing first frame: {frame_path}")
    graph = json.loads((WF / workflow_name).read_text(encoding="utf-8"))
    graph["3"]["inputs"]["noise_seed"] = 261000000 + int(shot[1:])
    graph["7"]["inputs"]["length"] = 195
    graph["7"]["inputs"]["prompt"] = PROMPTS[shot]
    graph["14"]["inputs"]["filename_prefix"] = f"逍遥仙重制/{shot}_{title}_PDD8"
    graph["20"]["inputs"]["image"] = f"逍遥仙/关键帧/{frame_name}"
    graph.pop("6", None)
    graph.pop("12", None)
    graph["13"]["inputs"].pop("audio", None)
    out = WF / f"{shot}_I2VA_PDD8_finale_api.json"
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    requests.get(API + "/system_stats", timeout=5).raise_for_status()
    result = requests.post(API + "/prompt", json={"prompt": graph, "client_id": str(uuid.uuid4())}, timeout=60)
    result.raise_for_status()
    payload = result.json()
    CHECK.mkdir(parents=True, exist_ok=True)
    (CHECK / f"{shot}_submit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"shot": shot, "workflow": str(out), **payload}, ensure_ascii=False))


if __name__ == "__main__":
    main()
