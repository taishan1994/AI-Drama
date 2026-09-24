"""提交《逍遥仙》S05；仅在ComfyUI和CUDA已经恢复时执行。"""
from pathlib import Path
import json
import sys
import uuid
import requests

API = "http://127.0.0.1:8188"
ROOT = Path("/data/ssd2/gongoubo/aijuman/音乐mv/逍遥仙")
WORKFLOW = ROOT / "工作流/S05_I2VA_PDD8_api.json"
LOG = ROOT / "检查/S05_submit.json"

try:
    requests.get(API + "/system_stats", timeout=5).raise_for_status()
except Exception as exc:
    raise SystemExit(f"ComfyUI未就绪: {exc}")

workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
response = requests.post(
    API + "/prompt",
    json={"prompt": workflow, "client_id": str(uuid.uuid4())},
    timeout=60,
)
response.raise_for_status()
result = response.json()
LOG.write_text(
    json.dumps({"prompt_id": result.get("prompt_id"), "number": result.get("number")}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps(result, ensure_ascii=False))
