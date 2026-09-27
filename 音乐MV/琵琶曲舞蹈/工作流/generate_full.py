"""Generate a full MiniMax-H3 duet in six memory-safe, pose-continuous chunks."""
from pathlib import Path
import argparse, json, shutil, subprocess, time, urllib.request
import cv2

P = Path(__file__).resolve().parents[1]
COMFY = P.parents[2] / "ComfyUI"
INPUT = COMFY / "input"
API = "http://127.0.0.1:8188"
BASE = P / "工作流/H3_5秒输出_15秒参考_API.json"
GUIDE = P / "处理/动作参考_目标舞台.mp4"
MASTER_AUDIO = P / "素材/原始音频.m4a"
KEYFRAME0 = INPUT / "pipa_duet_keyframe.png"
SEGMENT_FRAMES = 124
FINAL_SEGMENT_FRAMES = 56  # H3-valid 2.33s chunk; final output is trimmed to the 2s source tail.
FPS = 24

def frames_for(index):
    return FINAL_SEGMENT_FRAMES if index == 5 else SEGMENT_FRAMES

def request(path, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(API + path, data=body,
                                 headers={"Content-Type": "application/json"} if body else {})
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.load(response)

def prepare_segment(index):
    name = f"pipa_full_{index:02d}"
    video_path = INPUT / f"{name}_motion.mp4"
    audio_path = INPUT / f"{name}_audio.wav"
    cap = cv2.VideoCapture(str(GUIDE))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    start = index * SEGMENT_FRAMES
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    frames = []
    frame_count = frames_for(index)
    for _ in range(frame_count):
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame)
    cap.release()
    if not frames:
        raise RuntimeError(f"No motion-guide frames at segment {index}; guide has {total} frames")
    while len(frames) < frame_count:
        frames.append(frames[-1].copy())
    height, width = frames[0].shape[:2]
    writer = cv2.VideoWriter(str(video_path), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (width, height))
    for frame in frames:
        writer.write(frame)
    writer.release()
    start_time = start / FPS
    duration = frame_count / FPS
    # Keep exact soundtrack offsets. The final short source tail is padded for
    # H3's fixed 124-frame chunk and trimmed back during final assembly.
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{start_time:.9f}", "-i", str(MASTER_AUDIO),
           "-t", f"{duration:.9f}", "-af", "apad=pad_dur=5", "-ar", "32000", "-ac", "2",
           "-c:a", "pcm_s16le", str(audio_path)]
    subprocess.run(cmd, check=True)
    return video_path.name, audio_path.name

def prompt_for(index):
    start = index * SEGMENT_FRAMES / FPS
    end = start + frames_for(index) / FPS
    return f"""subject_definitions:
<Subject 1> Qingyi is the adult woman in teal in <Picture 1>, with a long oval face, high bun, jade pin, teal jade Hanfu, and ivory fan. Keep her face, outfit, and fan consistent in every segment.
<Subject 2> Hongyi is the distinct adult woman in vermilion in <Picture 1>, with a rounder face, half-up hair, gold floral ornaments, vermilion Hanfu, and ivory fan. Keep her face, outfit, and fan consistent in every segment.
<Picture 1> The exact full-scene start-frame composition for this segment: both women on the moonlit pavilion stage and exactly one wooden chair at center. Continue from this pose and preserve this stage.
<Audio 1> The original music excerpt paired with <Video 1>, from source time {start:.3f} to {min(end,27.834):.3f} seconds. It supplies the exact rhythm and phrase timing.
<Video 1> A motion guide composited over the final moonlit pavilion background. The teal and vermilion silhouettes show only the two dancers' source choreography and spatial paths for this time window. Do not reproduce silhouettes or flat cutout colors; render both realistic women as shown together in <Picture 1>.

summary:
Photorealistic 9:16 Chinese historical dance film, segment {index+1} of 6, source time {start:.3f}-{min(end,27.834):.3f}s. Preserve continuity with the provided start frame, exact choreography timing from the guide, two distinct adult women, and only one chair.

retention_analysis:
The stage remains the same moonlit waterside pavilion in every frame: fixed wooden columns, two warm lanterns, moonlit pond, distant mountains, glossy wood floor, and a single central carved wooden chair. The entire frame stays photographic and warmly lit; never turn the scene gray, white, foggy, or into a studio. No original studio background, ceiling, floor, text, or watermarks. Keep exactly two women and exactly one physical chair. Qingyi retains her teal costume, jade pin, oval face, and fan. Hongyi retains her vermilion costume, gold floral ornaments, rounder face, and fan. They stay separate and recognizable through turns and crossings. No duplicate, reflected, partial, ghosted, or extra chair; no stools, tables, benches, props, or people.

detailed_description:
[Continuous shot {index+1}, {start:.3f}-{min(end,27.834):.3f}s of source choreography] Begin in the exact complete scene shown in <Picture 1>; never begin with solo studio portraits or a blank gray scene. Continue directly from this two-person pose. Transfer the fan dance, weight shifts, turns, bows, arm sweeps, chair approaches, and footwork in the same order and rhythm as <Video 1>. The colored silhouettes are motion guides only and must become the two natural adult women shown together in <Picture 1>, dressed in realistic teal and vermilion Hanfu. Keep the single chair stationary at center and preserve believable hand-to-chair contact. Keep both dancers full-body and grounded on the floor. Camera stays locked in the same portrait full-body framing. The set dressing and light remain stable and richly photorealistic; no scene cuts within a segment. Maintain the original music timing from <Audio 1>, with no dialogue or added sounds.

overall_soundscape:
Only the corresponding original music excerpt <Audio 1>, with the exact source start time and beat alignment; no dialogue or extra sounds.

non_diegetic_music:
Preserve the original music excerpt and its timing exactly."""

def make_workflow(index, keyframe, video_name, audio_name):
    g = json.loads(BASE.read_text())
    g["6"]["inputs"].update({
        "width": 768, "height": 1344, "length": frames_for(index),
        "prompt": prompt_for(index),
        "ref_images.ref_image_0": ["18", 0],
        "ref_videos.ref_video_0": ["21", 0],
        "ref_video_audios.ref_video_audio_0": ["22", 0],
    })
    g["6"]["inputs"].pop("ref_images.ref_image_1", None)
    g["6"]["inputs"].pop("ref_images.ref_image_2", None)
    g["18"]["inputs"]["image"] = keyframe.name
    g["20"]["inputs"]["file"] = video_name
    g["22"]["inputs"]["audio"] = audio_name
    g["23"]["inputs"]["audio"] = audio_name
    g["15"]["inputs"]["filename_prefix"] = f"video/pipa_duet/full_seg{index:02d}"
    g["10"]["inputs"]["noise_seed"] = 76218797 + index
    return g

def get_mp4(history):
    for item in history.get("outputs", {}).get("15", {}).get("images", []):
        if isinstance(item, dict) and item.get("filename", "").endswith(".mp4"):
            return item
    return None

def run(first, last):
    (P / "视频/分段").mkdir(parents=True, exist_ok=True)
    keyframe = KEYFRAME0 if first == 0 else INPUT / f"pipa_full_keyframe_after_{first-1:02d}.png"
    for i in range(first, last):
        video_name, audio_name = prepare_segment(i)
        graph = make_workflow(i, keyframe, video_name, audio_name)
        workflow_path = P / "工作流" / f"H3_全片第{i+1:02d}段_API.json"
        workflow_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2))
        queued = request("/prompt", {"prompt": graph, "client_id": "pipa-duet-film"})
        pid = queued["prompt_id"]
        start_seconds = i * SEGMENT_FRAMES / FPS
        (P / "工作流" / f"H3_全片第{i+1:02d}段任务.json").write_text(json.dumps({"prompt_id":pid,"segment":i,"start_time":start_seconds,"frames":frames_for(i)},ensure_ascii=False,indent=2))
        print(f"queued segment {i+1}/6 ({start_seconds:.3f}s, {frames_for(i)} frames), prompt {pid}", flush=True)
        while True:
            history = request("/history/" + pid).get(pid)
            if history:
                status = history.get("status", {})
                if status.get("status_str") == "error":
                    (P / "工作流" / f"H3_全片第{i+1:02d}段错误.json").write_text(json.dumps(history,ensure_ascii=False,indent=2))
                    raise RuntimeError(f"segment {i+1} failed: {status}")
                if status.get("completed"):
                    (P / "工作流" / f"H3_全片第{i+1:02d}段历史.json").write_text(json.dumps(history,ensure_ascii=False,indent=2))
                    item = get_mp4(history)
                    if item is None:
                        raise RuntimeError(f"segment {i+1} completed with no MP4 output")
                    src = COMFY / "output" / item.get("subfolder", "") / item["filename"]
                    dst = P / "视频/分段" / f"段{i+1:02d}_待检查.mp4"
                    shutil.copy2(src, dst)
                    print(f"saved {dst}", flush=True)
                    if i < 5:
                        keyframe = INPUT / f"pipa_full_keyframe_after_{i:02d}.png"
                        cap = cv2.VideoCapture(str(dst))
                        count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, count - 1))
                        ok, frame = cap.read(); cap.release()
                        if not ok:
                            raise RuntimeError(f"cannot extract final frame from {dst}")
                        if not cv2.imwrite(str(keyframe), frame):
                            raise RuntimeError(f"cannot write continuation keyframe {keyframe}")
                    break
            time.sleep(8)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=0, help="zero-based first segment")
    parser.add_argument("--last", type=int, default=6, help="exclusive zero-based end segment")
    args = parser.parse_args()
    run(args.first, args.last)
