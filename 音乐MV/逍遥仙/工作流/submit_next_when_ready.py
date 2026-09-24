"""提交《逍遥仙》下一个缺失镜头；每次只提交一个，生成后须人工验收。"""
from pathlib import Path
import json
import sys
import uuid
import requests

API = "http://127.0.0.1:8188"
ROOT = Path("/data/ssd2/gongoubo/aijuman/音乐mv/逍遥仙")
SEG = ROOT / "视频/片段"
WORKFLOWS = [
    ("S05", "S05_云海高台_静音验收版.mp4"),
    ("S06", "S06_云中山脊_静音验收版.mp4"),
    ("S07", "S07_云海酒盏_静音验收版.mp4"),
    ("S08", "S08_人间小院_静音验收版.mp4"),
    ("S09", "S09_四季院落_静音验收版.mp4"),
    ("S10", "S10_出院门_静音验收版.mp4"),
    ("S11", "S11_山河纸鹤_静音验收版.mp4"),
    ("S12", "S12_山顶落脚_静音验收版.mp4"),
    ("S13", "S13_回望灯火_静音验收版.mp4"),
    ("S14", "S14_山河纸灯收束_静音验收版.mp4"),
]

try:
    requests.get(API + "/system_stats", timeout=5).raise_for_status()
except Exception as exc:
    raise SystemExit(f"ComfyUI未就绪，不提交任务: {exc}")

for shot, accepted_name in WORKFLOWS:
    if (SEG / accepted_name).exists():
        continue
    workflow_path = ROOT / f"工作流/{shot}_I2VA_PDD8_api.json"
    if not workflow_path.exists():
        raise SystemExit(f"缺少 {shot} 工作流: {workflow_path}")
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    result = requests.post(
        API + "/prompt",
        json={"prompt": workflow, "client_id": str(uuid.uuid4())},
        timeout=60,
    )
    result.raise_for_status()
    payload = result.json()
    log_path = ROOT / f"检查/{shot}_submit.json"
    log_path.write_text(
        json.dumps({"shot": shot, "prompt_id": payload.get("prompt_id"), "number": payload.get("number")}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"submitted": shot, **payload}, ensure_ascii=False))
    break
else:
    print("S05-S14 均已有静音验收片段，无需提交。")
