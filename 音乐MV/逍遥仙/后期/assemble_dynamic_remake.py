"""Assemble the accepted R00-R27 remake, then mux the original song and lyrics."""
from pathlib import Path
import subprocess
import tempfile


ROOT = Path("/data/ssd2/gongoubo/aijuman/音乐mv/逍遥仙")
R_OUT = Path("/data/ssd2/gongoubo/aijuman/h3/ComfyUI/output/逍遥仙重制")
ARCHIVE = ROOT / "视频/尾声重制"
AUDIO = ROOT / "素材/音频/逍遥仙_筷子兄弟_纯歌曲版.m4a"
SRT = ROOT / "字幕/逍遥仙_R00-R27_歌词校正.srt"
FONT = Path("/data/ssd2/gongoubo/aijuman/耳中人短剧/subtitles/fonts/NotoSerifCJKsc-Regular.otf")
TITLE = ROOT / "封面/逍遥仙_片尾艺术字透明.png"
OUT_BASE = ROOT / "视频/逍遥仙_R00-R27动态重制_v2_无字幕底片.mp4"
OUT_SUBBED = ROOT / "视频/逍遥仙_R00-R27动态重制_v2_歌词字幕.mp4"

SHOTS = [
    ("R00_片头风起纸灯_PDD8_00001_.mp4", R_OUT),
    ("R01_渡口显现_PDD8_00001_.mp4", R_OUT),
    ("R02_行旅者入渡口_PDD8_00002_.mp4", R_OUT),
    ("R03_抬头望山_PDD8_00004_.mp4", R_OUT),
    ("R04_酒壶路引_PDD8_00002_.mp4", R_OUT),
    ("R05_拿壶饮酒_PDD8_00002_.mp4", R_OUT),
    ("R06_雨夜石阶_PDD8_00001_.mp4", R_OUT),
    ("R07_雨中上行_PDD8_00001_.mp4", R_OUT),
    ("R08_雨墨纸片_PDD8_00004_.mp4", R_OUT),
    ("R09_墨纸成形_PDD8_00002_.mp4", R_OUT),
    ("R10_纸页引路_PDD8_00001_.mp4", R_OUT),
    ("R11_纸页旋升_PDD8_00001_.mp4", R_OUT),
    ("R12_墨纸飞鸟_PDD8_00001_.mp4", R_OUT),
    ("R13_高台远景_角色板锁定.mp4", ARCHIVE),
    ("R14_高台风云_角色板锁定.mp4", ARCHIVE),
    ("R15_高台近景离开.mp4", ARCHIVE),
    ("R16_山脊持续前行.mp4", ARCHIVE),
    ("R17_酒盏倒影转场.mp4", ARCHIVE),
    ("R18_夜院落座.mp4", ARCHIVE),
    ("R19_院中路引.mp4", ARCHIVE),
    ("R20_院中四季_春夏秋冬再回春.mp4", ARCHIVE),
    ("R21_院中冬雪融春_背包连续.mp4", ARCHIVE),
    ("R22_院门前停步.mp4", ARCHIVE),
    ("R23_纸鹤引路.mp4", ARCHIVE),
    ("R24_山河长卷展开.mp4", ARCHIVE),
    ("R25_山顶站定.mp4", ARCHIVE),
    ("R26_回望人间灯火.mp4", ARCHIVE),
    ("R27_纸灯收束_无片名底片.mp4", ARCHIVE),
]


def run(args):
    subprocess.run(args, check=True)


def duration(path):
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], text=True).strip())


def probe_streams(path):
    import json
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path),
    ], text=True))["streams"]


missing = [str(folder / name) for name, folder in SHOTS if not (folder / name).is_file()]
if missing:
    raise SystemExit("缺少指定验收镜头：\n" + "\n".join(missing))
for path in (AUDIO, SRT, FONT, TITLE):
    if not path.is_file():
        raise SystemExit(f"缺少必要文件：{path}")
if OUT_BASE.exists() or OUT_SUBBED.exists():
    raise SystemExit("目标文件已存在；为避免覆盖，请先指定新的输出名。")

ROOT.joinpath("视频").mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="xiaoyaoxian_R00_R27_") as temp:
    temp = Path(temp)
    normalized = []
    for idx, (name, folder) in enumerate(SHOTS):
        source = folder / name
        target_duration = 8.0 if idx < 27 else 8.618667
        streams = probe_streams(source)
        video_streams = [s for s in streams if s.get("codec_type") == "video"]
        audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
        if len(video_streams) != 1 or audio_streams:
            raise SystemExit(f"验收素材必须是单路静音视频：{source}")
        if (video_streams[0].get("width"), video_streams[0].get("height")) != (1344, 768):
            raise SystemExit(f"画幅不是 1344×768：{source}")
        if duration(source) + 0.001 < target_duration:
            raise SystemExit(f"镜头时长不足 {target_duration:.3f}s：{source}")
        part = temp / f"part_{idx:02d}.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(source), "-an", "-vf", "fps=24",
            "-t", f"{target_duration:.6f}", "-c:v", "libx264",
            "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-video_track_timescale", "24000", str(part),
        ])
        normalized.append(part)

    concat_file = temp / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in normalized) + "\n",
        encoding="utf-8",
    )
    silent = temp / "picture.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-an", "-c:v", "copy", "-movflags", "+faststart", str(silent),
    ])

    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(silent), "-i", str(AUDIO), "-loop", "1", "-framerate", "24",
        "-i", str(TITLE),
        "-filter_complex",
        "[2:v]scale=780:-1,format=rgba,fade=t=in:st=216:d=0.8:alpha=1[title];"
        "[0:v][title]overlay=x=(W-w)/2:y=25:eval=frame:"
        "enable='gte(t,216)':format=auto[v]",
        "-map", "[v]", "-map", "1:a:0",
        "-t", "224.618667", "-c:v", "libx264", "-preset", "medium",
        "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac",
        "-b:a", "256k", "-movflags", "+faststart", str(OUT_BASE),
    ])

    escaped_srt = str(SRT).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    escaped_fontdir = str(FONT.parent).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    subtitles_filter = (
        f"subtitles='{escaped_srt}':fontsdir='{escaped_fontdir}':force_style="
        "'FontName=Noto Serif CJK SC,FontSize=48,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H80000000,BackColour=&H99000000,BorderStyle=3,"
        "Outline=0,Shadow=0,Alignment=2,MarginV=52'"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(OUT_BASE), "-vf", subtitles_filter,
        "-map", "0:v:0", "-map", "0:a:0", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", str(OUT_SUBBED),
    ])

print(OUT_BASE)
print(OUT_SUBBED)
