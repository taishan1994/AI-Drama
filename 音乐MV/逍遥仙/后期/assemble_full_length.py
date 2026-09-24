"""Build the full-length silent picture edit from accepted clips, then add the song."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path("/data/ssd2/gongoubo/aijuman/音乐mv/逍遥仙")
SEG = ROOT / "视频/片段"
OUT = ROOT / "视频/逍遥仙_完整MV_无字幕底片.mp4"
AUDIO = ROOT / "素材/音频/逍遥仙_筷子兄弟_纯歌曲版.m4a"

# Durations follow the locked shot table and cover the full 3:45 arrangement.
SHOTS = [
    ("S00_片头风起纸灯_静音验收版.mp4", 10.0),
    ("S01_渡口背影_静音验收版_final.mp4", 12.0),
    ("S02_酒壶路引_静音验收版.mp4", 8.0),
    ("S03_雨夜山路_静音验收版_final.mp4", 18.0),
    ("S04A_碎纸石阶_静音验收版.mp4", 8.5),
    ("S04B_纸鸟断桥_静音验收版.mp4", 8.5),
    ("S05_云海高台_静音验收版.mp4", 18.0),
    ("S06_云中山脊_静音验收版.mp4", 18.0),
    ("S07_云海酒盏_静音验收版.mp4", 12.0),
    ("S08_人间小院_静音验收版.mp4", 17.0),
    ("S09_四季院落_静音验收版.mp4", 20.0),
    ("S10_出院门_静音验收版.mp4", 18.0),
    ("S11_山河纸鹤_静音验收版.mp4", 17.0),
    ("S12_山顶落脚_静音验收版.mp4", 17.0),
    ("S13_回望灯火_静音验收版.mp4", 17.0),
    ("S14_山河纸灯收束_静音验收版.mp4", 6.0),
]

missing = [name for name, _ in SHOTS if not (SEG / name).exists()]
if missing:
    raise SystemExit("缺少验收片段:\n" + "\n".join(missing))
if not AUDIO.exists():
    raise SystemExit(f"缺少歌曲音频: {AUDIO}")

with tempfile.TemporaryDirectory(prefix="xiaoyaoxian_full_") as td:
    td = Path(td)
    parts = []
    for index, (name, target) in enumerate(SHOTS):
        src = SEG / name
        probe = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(src)
        ], text=True).strip()
        source_duration = float(probe)
        factor = target / source_duration
        part = td / f"part_{index:02d}.mp4"
        # Time-remap each accepted silent clip to the locked music timeline.
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src), "-an", "-vf", f"setpts={factor:.12f}*PTS,fps=24",
            "-t", f"{target:.3f}", "-c:v", "libx264", "-preset", "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", str(part)
        ], check=True)
        parts.append(part)

    concat = td / "concat.txt"
    concat.write_text("\n".join(f"file '{p.as_posix()}'" for p in parts) + "\n", encoding="utf-8")
    silent = td / "silent.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
        "-safe", "0", "-i", str(concat), "-an", "-c:v", "libx264", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent)
    ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent),
        "-i", str(AUDIO), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart",
        str(OUT)
    ], check=True)
print(OUT)
