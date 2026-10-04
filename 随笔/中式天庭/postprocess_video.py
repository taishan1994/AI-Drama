#!/usr/bin/env python3
"""Stitch the five silent image-to-video renders and optionally mux a score."""
import argparse
import json
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
VIDEO_DIR = PROJECT / "视频"
SEGMENT_DIR = VIDEO_DIR / "分段"
WORK = VIDEO_DIR / "_中间文件"
STITCHED = VIDEO_DIR / "中式天庭_无配乐版.mp4"
FINAL = VIDEO_DIR / "中式天庭_配乐成片.mp4"
SEGMENTS = [
    "01_云上天门｜低机位推进.mp4", "02_云海仙宫群｜高空穿行.mp4", "03_晨雾宫阁｜阳台横移.mp4",
    "04_天庭仪典广场｜中轴升推.mp4", "05_夕照天宫｜悬崖仰望.mp4",
]


def run(args):
    subprocess.run(args, check=True)


def probe(path):
    data = json.loads(subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
        "-of", "json", str(path),
    ], check=True, capture_output=True, text=True).stdout)
    duration = float(data["format"]["duration"])
    video = next(stream for stream in data["streams"] if stream["codec_type"] == "video")
    return duration, video


def stitch():
    WORK.mkdir(parents=True, exist_ok=True)
    missing = [name for name in SEGMENTS if not (SEGMENT_DIR / name).exists()]
    if missing:
        raise FileNotFoundError(f"missing rendered segments: {missing}")
    normalized = []
    durations = []
    for index, name in enumerate(SEGMENTS, 1):
        source = SEGMENT_DIR / name
        target = WORK / f"silent_{index:02d}.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-i", str(source),
            "-map", "0:v:0", "-an", "-vf", "scale=1344:768:force_original_aspect_ratio=decrease,pad=1344:768:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-movflags", "+faststart", str(target),
        ])
        duration, video = probe(target)
        if video["width"] != 1344 or video["height"] != 768 or video["r_frame_rate"] != "24/1":
            raise RuntimeError(f"unexpected normalized clip format for {target.name}: {video}")
        normalized.append(target)
        durations.append(duration)
    concat_list = WORK / "concat.txt"
    concat_list.write_text("".join(f"file '{path.as_posix()}'\n" for path in normalized), encoding="utf-8")
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-map", "0:v:0", "-an", "-c:v", "copy", "-movflags", "+faststart", str(STITCHED),
    ])
    total, _ = probe(STITCHED)
    print(f"stitched silent video: {STITCHED} ({total:.3f}s; segments {', '.join(f'{d:.3f}' for d in durations)}s)")


def mux(music):
    if not STITCHED.exists():
        raise FileNotFoundError(f"stitch the segments first: {STITCHED}")
    if not music.exists():
        raise FileNotFoundError(music)
    duration, _ = probe(STITCHED)
    fade_out = max(0.0, duration - 3.0)
    audio_filter = f"loudnorm=I=-18:TP=-1.5:LRA=11,afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out:.3f}:d=3,apad,atrim=duration={duration:.3f}"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning", "-i", str(STITCHED), "-i", str(music),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-af", audio_filter, "-t", f"{duration:.3f}", "-movflags", "+faststart", str(FINAL),
    ])
    total, _ = probe(FINAL)
    print(f"final video with continuous score: {FINAL} ({total:.3f}s)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stitch-only", action="store_true")
    parser.add_argument("--music", type=Path)
    args = parser.parse_args()
    if not STITCHED.exists():
        stitch()
    if args.music:
        mux(args.music.resolve())
    elif not args.stitch_only:
        print(f"silent stitched video ready: {STITCHED}; pass --music after generating the score to create the final MP4")


if __name__ == "__main__":
    main()
