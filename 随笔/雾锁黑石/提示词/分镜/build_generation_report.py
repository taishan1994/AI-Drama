#!/usr/bin/env python3
"""Build the per-shot MiniMax-H3 generation report from source data and manifests."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPTS = ROOT / "提示词" / "分镜"
OUT = ROOT / "分镜视频" / "雾锁黑石_分镜生成报告.md"
SHOTS = json.loads((PROMPTS / "script_shots_with_assets.json").read_text())

manifest_files = [ROOT / "分镜视频" / "生成清单.json", Path("/tmp/h3-gpu1-manifest.json")]
records = {}
for path in manifest_files:
    if not path.exists():
        continue
    data = json.loads(path.read_text())
    for item in data.get("shots", []):
        old = records.get(item["shot"])
        # Successful renders supersede stale attempts, including the old shot 25 entry.
        if old is None or item.get("status") == "success" or old.get("status") != "success":
            records[item["shot"]] = item

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
lines = [
    "# 雾锁黑石分镜视频生成报告",
    "",
    f"> 生成状态快照：{now}。所有分镜生成完成后重新运行 `python3 build_generation_report.py` 更新本报告。",
    "",
    "## 全局模型与流程",
    "",
    "- 视频模型：MiniMax-H3 Ref2VA INT8 ConvRot（`minimax_h3_ref2va_pruned_int8_convrot.safetensors`）。",
    "- 加速：官方 MiniMax-H3 Ref2VA 8-step Acc LoRA，8 步 Euler 采样。",
    "- 文本编码器：Qwen3-VL-32B MiniMax-H3 INT8 ConvRot。",
    "- 提示词重写：本地 Qwen3.5-4B GGUF，依照 `minimax-h3-writing` skill 与 Ref2VA 指南，生成六段结构并核验引用标签、对白和时长。",
    "- 流程：分镜原始描述 + 对应图片资产 → skill 约束下的 H3 提示词重写 → H3 Ref2VA 采样 → VAE 解码 → MP4 保存。",
    "- 输出目标：1344×768，24 fps；镜头时长按分镜设定。部分镜头以独立资产图片作为 `<Picture n>` 引用。",
    "",
    "## 镜头明细",
]

for shot in SHOTS:
    n = shot["shot"]
    rec = records.get(n, {})
    status = rec.get("status", "pending")
    duration = shot.get("duration", rec.get("duration", "未知"))
    optimized_path = PROMPTS / "optimized_prompts" / f"shot_{n:02}_optimized.txt"
    optimized = optimized_path.read_text().strip() if optimized_path.exists() else "（优化提示词文件缺失）"
    source_prompt = shot.get("source_description", shot.get("visual_description", ""))
    lines += [
        "",
        f"### 镜头 {n:02}（{shot.get('start', '?')}–{shot.get('end', '?')}，设定 {duration} 秒）",
        "",
        f"- 生成状态：`{status}`。",
        f"- 成片：`{rec.get('video', str(ROOT / '分镜视频' / f'shot_{n:02}.mp4'))}`。",
        *([f"- 后期裁剪：{rec['edit_note']}（成片时长 {rec.get('actual_duration', '未知')} 秒）。"] if rec.get("edit_note") else []),
        f"- 资产文件：{', '.join(f'`资产/{x}`' for x in shot.get('asset_files', [])) or '无'}。",
        f"- ComfyUI 输入名：{', '.join(f'`{x}`' for x in shot.get('comfy_input_files', [])) or '无'}。",
        f"- 结束转场：{shot.get('transition_to_next', '无')} ",
        "",
        "**原始分镜描述（用户输入）**",
        "",
        "```text",
        source_prompt,
        "```",
        "",
        f"**优化后 MiniMax-H3 prompt**（[`{optimized_path.name}`]({optimized_path.relative_to(ROOT)}))",
        "",
        "```text",
        optimized,
        "```",
    ]

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n")
print(f"Wrote {OUT} ({len(SHOTS)} shots; successful records: {sum(x.get('status') == 'success' for x in records.values())})")
