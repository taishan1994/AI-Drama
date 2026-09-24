"""Submit character-locked Ref2VA shots for the 逍遥仙 remake."""
from pathlib import Path
import copy, json, sys, uuid, requests

API = "http://127.0.0.1:8188"
ROOT = Path("/data/ssd2/gongoubo/aijuman/音乐mv/逍遥仙")
WF_DIR = ROOT / "工作流"
CHECK = ROOT / "检查/动态重制"
BASE = Path("/data/ssd2/gongoubo/aijuman/短剧/尸变/workflows/S05_走向后院_Ref2VA_PDD8_api.json")

SHOTS = {
    "R13": ("R13_角色板锁定_高台首帧.png", "高台远景_Ref2VA角色锁定"),
    "R14": ("R14_角色板锁定_高台首帧.png", "高台风云_Ref2VA角色锁定"),
    "R15": ("R15_角色板锁定_近景首帧.png", "山脊行走_Ref2VA角色锁定"),
}

PROMPTS = {
    "R13": """[reference generation] 图片一和图片二是同一张角色板锁定的高台首帧，必须保持相同人物、相同石碑、相同老松和相同月夜构图，不得重新设计人物。上美影二维手绘动画，纸张纹理、墨线、平涂色块、电影胶片颗粒。唯一行旅者必须始终保持：木簪高髻、长黑发披背、蓝灰分层外袍、白色破边内层、赭红腰封、黑布靴、右腕红绳、编织肩带和一个圆形藤背包。0到2秒人物右手扶住高石碑，衣摆和发尾被冷风轻吹；2到5秒镜头缓慢向右侧横移并轻微拉远，只露出原有两块石碑和左侧老松，人物始终落地；5到8秒人物转头望向云海但不露正脸，保持同一服装、发型、背包和体态。只出现一个人物、两块石碑、一棵老松和云海；禁止复制石碑、第二背包、第二人物、鸟群、船、日出日落、海面、文字和字幕。生成静音视频。""",
    "R14": """[reference generation] 图片一和图片二是同一张角色板锁定的高台首帧，必须作为全片人物和空间硬参考。上美影二维手绘动画，冷蓝月夜、墨线和电影胶片颗粒。唯一行旅者保持木簪高髻、长黑发、蓝灰外袍、白色破边内层、赭红腰封、黑布靴、右腕红绳、编织肩带和一个圆形藤背包。镜头固定在中后景：0到2秒右手扶石碑；2到5秒冷风从右向左吹动衣摆、红腰带和发尾，人物脚底不移动；5到8秒云雾在背景缓慢流动，人物仍站在原位。严格只保留首帧中的两块石碑和一棵老松，不生成其他石碑、鸟、船、人物、水面或日落。不得变脸、换发型、换装、增加背包、出现正面脸或可读文字。生成静音视频。""",
    "R15": """[reference generation] 图片一和图片二是同一张角色板锁定的山脊近景首帧，必须作为人物身份和构图硬参考。上美影二维手绘动画，冷蓝夜色、墨线、纸张纹理和电影胶片颗粒。唯一行旅者始终保持木簪高髻、披背长发、蓝灰分层外袍、白色破边内层、赭红腰封、黑布靴、右腕红绳、编织肩带和一个圆形藤背包。固定后侧近景机位，不展示天空、太阳、海面或远景；0到2秒左脚抬起；2到5秒人物沿同一石径向前走两小步，双脚与石面接触；5到8秒衣摆、发尾和腰带被风吹动，镜头只做极小幅度跟随。背景只保留首帧中的岩石小径和低矮松枝，不得出现船、石碑复制、日落、第二人物、第二背包、正面脸、变脸、换装、文字或字幕。生成静音视频。""",
}

def build(shot):
    first, title = SHOTS[shot]
    base = json.loads(BASE.read_text(encoding="utf-8"))
    base["1"]["inputs"]["unet_name"] = "MiniMax_H3_Ref2VA_pruned_int8_convrot.safetensors"
    base["3"]["inputs"]["noise_seed"] = 271000000 + int(shot[1:])
    node = base["7"]
    node["class_type"] = "MiniMaxH3ReferenceToVideo"
    node["inputs"]["prompt"] = PROMPTS[shot]
    node["inputs"]["width"] = 1344
    node["inputs"]["height"] = 768
    node["inputs"]["length"] = 195
    node["inputs"]["ref_image_size"] = "max"
    node["inputs"]["ref_images.ref_image_0"] = ["20", 0]
    node["inputs"]["ref_images.ref_image_1"] = ["21", 0]
    base["15"]["inputs"]["pdd_file"] = "MiniMax-H3-Ref2VA-Acc-8Step.safetensors"
    base["14"]["inputs"]["filename_prefix"] = f"逍遥仙重制/{shot}_{title}_PDD8"
    base["20"]["inputs"]["image"] = f"逍遥仙/关键帧/{first}"
    base["21"]["inputs"]["image"] = f"逍遥仙/关键帧/{first}"
    # silent video: keep the audio VAE input required by Ref2VA, but do not render audio.
    base["13"]["inputs"].pop("audio", None)
    base.pop("12", None)
    path = WF_DIR / f"{shot}_Ref2VA_PDD8_character_locked_api.json"
    path.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    result = requests.post(API + "/prompt", json={"prompt": base, "client_id": str(uuid.uuid4())}, timeout=60)
    result.raise_for_status()
    payload = result.json()
    (CHECK / f"{shot}_Ref2VA_submit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"shot": shot, "workflow": str(path), **payload}, ensure_ascii=False))

if __name__ == "__main__":
    shot = sys.argv[1] if len(sys.argv) > 1 else "R13"
    if shot not in SHOTS:
        raise SystemExit(f"unknown shot: {shot}")
    build(shot)
