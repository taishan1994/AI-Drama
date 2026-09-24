"""《逍遥仙》最终合成：只接收已验收静音片段，最后统一挂接纯净歌曲。"""
from pathlib import Path
import subprocess
import sys

ROOT = Path("/data/ssd2/gongoubo/aijuman/音乐mv/逍遥仙")
SEG = ROOT / "视频/片段"
AUDIO = ROOT / "素材/音频/逍遥仙_筷子兄弟.m4a"
OUT = ROOT / "视频/逍遥仙_无舞蹈MV_无字幕底片.mp4"
ORDER = [
    "S00_片头风起纸灯_静音验收版.mp4",
    "S01_渡口背影_静音验收版_final.mp4",
    "S02_酒壶路引_静音验收版.mp4",
    "S03_雨夜山路_静音验收版_final.mp4",
    "S04A_碎纸石阶_静音验收版.mp4",
    "S04B_纸鸟断桥_静音验收版.mp4",
    "S05_云海高台_静音验收版.mp4",
    "S06_云中山脊_静音验收版.mp4",
    "S07_云海酒盏_静音验收版.mp4",
    "S08_人间小院_静音验收版.mp4",
    "S09_四季院落_静音验收版.mp4",
    "S10_出院门_静音验收版.mp4",
    "S11_山河纸鹤_静音验收版.mp4",
    "S12_山顶落脚_静音验收版.mp4",
    "S13_回望灯火_静音验收版.mp4",
    "S14_山河纸灯收束_静音验收版.mp4",
]

missing = [name for name in ORDER if not (SEG / name).exists()]
if missing:
    print("缺少验收片段：", file=sys.stderr)
    print("\n".join(missing), file=sys.stderr)
    raise SystemExit(2)
if not AUDIO.exists():
    raise SystemExit(f"缺少歌曲音频: {AUDIO}")

concat = ROOT / "后期/concat_silent.txt"
concat.write_text("\n".join(f"file '{(SEG / name).as_posix()}'" for name in ORDER) + "\n", encoding="utf-8")
silent = ROOT / "视频/逍遥仙_无舞蹈MV_静音拼接.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
    "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent),
], check=True)
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent), "-i", str(AUDIO),
    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
    "-shortest", "-movflags", "+faststart", str(OUT),
], check=True)
print(OUT)
