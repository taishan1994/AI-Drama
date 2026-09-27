#!/usr/bin/env python3
"""Convert the Pipa dance source video to a high-contrast deep monochrome MP4."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "素材" / "7621879784973062134.mp4"
DEFAULT_OUTPUT = ROOT / "处理" / "深度黑白" / "7621879784973062134_白模深度黑白.mp4"


def main() -> None:
    parser = argparse.ArgumentParser(description="视频转深度黑白格式，保留原音频")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if not args.input.exists():
        raise SystemExit(f"输入视频不存在: {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # 先去饱和并轻度抹平纹理，再量化成少量灰阶；人物会变成接近白模的
    # 大块面，脸部、衣料和细小道具细节被压掉，只保留轮廓和动作关系。
    video_filter = (
        "hue=s=0," 
        "gblur=sigma=1.8," 
        "eq=contrast=2.25:brightness=0.06:gamma=1.08," 
        "lut=y='if(lt(val,72),12,if(lt(val,142),88,if(lt(val,205),178,245)))'"
    )
    command = [
        "ffmpeg", "-y", "-i", str(args.input),
        "-vf", video_filter,
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-map", "0:v:0", "-map", "0:a?", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(args.output),
    ]
    print("执行:", " ".join(command))
    subprocess.run(command, check=True)
    print(f"输出: {args.output}")


if __name__ == "__main__":
    main()
