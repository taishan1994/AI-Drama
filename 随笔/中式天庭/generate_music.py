#!/usr/bin/env python3
"""Generate one continuous instrumental score with the local ACE-Step XL-SFT workflow."""
import json
import shutil
import time
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
COMFY = Path("/nfs/FM/gongoubo/new_project/github/aigc/ComfyUI")
API = "http://127.0.0.1:8189"
VIDEO = PROJECT / "视频" / "中式天庭_无配乐版.mp4"
TAGS = """Original instrumental cinematic score for a Chinese mythological heavenly palace panorama, majestic, ethereal and spacious. Begin with delicate guqin harmonics, a breathy xiao flute melody and sparse distant bronze bells over a soft cloudlike pad. Gradually add warm low strings, restrained frame drums and a broad lyrical orchestral swell as the celestial city is revealed. Reach a noble, awe-filled peak without becoming bombastic, then resolve gently into sustained xiao and guqin tones. Around 72 BPM, coherent evolving arrangement, subtle dynamics, elegant Chinese pentatonic color, no vocals, no lyrics, no choir, no pop drums, no EDM, no abrupt sound effects. Smooth cinematic background score with a soft opening and a lingering resolved ending."""


def post(path, data=None):
    body = None if data is None else json.dumps(data, ensure_ascii=False).encode()
    request = urllib.request.Request(API + path, data=body,
        headers={"Content-Type": "application/json"} if body else {})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())


def video_duration(path):
    import subprocess
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def audio_graph(duration):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "acestep_v1.5_xl_sft_bf16.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3}},
        "3": {"class_type": "DualCLIPLoader", "inputs": {
            "clip_name1": "qwen_0.6b_ace15.safetensors",
            "clip_name2": "qwen_4b_ace15.safetensors", "type": "ace", "device": "default"}},
        "4": {"class_type": "TextEncodeAceStepAudio1.5", "inputs": {
            "clip": ["3", 0], "tags": TAGS, "lyrics": "", "seed": 928115,
            "bpm": 72, "duration": duration, "timesignature": "4", "language": "en",
            "keyscale": "E minor", "generate_audio_codes": True, "cfg_scale": 2.0,
            "temperature": 0.85, "top_p": 1.0, "top_k": 0, "min_p": 0.0}},
        "5": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["4", 0]}},
        "6": {"class_type": "EmptyAceStep1.5LatentAudio", "inputs": {"seconds": duration, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {
            "model": ["2", 0], "positive": ["4", 0], "negative": ["5", 0],
            "latent_image": ["6", 0], "seed": 928115, "steps": 50, "cfg": 7,
            "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "8": {"class_type": "VAELoader", "inputs": {"vae_name": "ace_1.5_vae.safetensors"}},
        "9": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["7", 0], "vae": ["8", 0]}},
        "10": {"class_type": "SaveAudio", "inputs": {
            "audio": ["9", 0], "filename_prefix": "audio/chinese_heaven/ACE_Step_1.5_XL_SFT"}},
    }


def find_audio(history):
    found = []
    def visit(value):
        if isinstance(value, dict):
            filename = value.get("filename")
            if isinstance(filename, str) and filename.lower().endswith((".flac", ".wav", ".mp3")):
                found.append(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(history.get("outputs", {}))
    return found


def main():
    if not VIDEO.exists():
        raise FileNotFoundError(f"stitch the five silent video segments first: {VIDEO}")
    duration = round(video_duration(VIDEO) / 0.04) * 0.04
    graph = audio_graph(duration)
    check = post("/object_info")
    required_nodes = ("UNETLoader", "DualCLIPLoader", "TextEncodeAceStepAudio1.5",
                      "EmptyAceStep1.5LatentAudio", "SaveAudio")
    missing = [name for name in required_nodes if name not in check]
    if missing:
        raise RuntimeError(f"ACE-Step ComfyUI nodes missing: {missing}")
    prompt_path = PROJECT / "state" / "music_api.json"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    output_dir = COMFY / "output"
    result = post("/prompt", {"prompt": graph, "client_id": "chinese-heaven-score"})
    if "prompt_id" not in result:
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    prompt_id = result["prompt_id"]
    log_path = PROJECT / "state" / "music_generation.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().astimezone().isoformat(timespec='seconds')} queued ACE-Step 1.5 XL-SFT instrumental score, duration={duration:.2f}s, prompt={prompt_id}"
    print(line, flush=True)
    log_path.write_text(line + "\n", encoding="utf-8")
    started = time.monotonic()
    while time.monotonic() - started < 3600:
        history = post(f"/history/{prompt_id}").get(prompt_id)
        if history:
            status = history.get("status", {})
            if status.get("completed"):
                audio = find_audio(history)
                if not audio:
                    candidates = list((output_dir / "audio" / "chinese_heaven").glob("ACE_Step_1.5_XL_SFT*.flac"))
                    if not candidates:
                        raise RuntimeError(f"score completed but no audio file is listed: {history.get('outputs')}")
                    item = {"filename": candidates[-1].name, "subfolder": "audio/chinese_heaven"}
                else:
                    item = audio[0]
                source = output_dir / item.get("subfolder", "") / item["filename"]
                target_dir = PROJECT / "音频"
                target_dir.mkdir(parents=True, exist_ok=True)
                target = target_dir / "中式天庭_ACE-Step_1.5_XL-SFT_纯器乐配乐.flac"
                shutil.copy2(source, target)
                with log_path.open("a", encoding="utf-8") as stream:
                    stream.write(f"completed: {target}\n")
                print(f"completed: {target}", flush=True)
                return
            if status.get("status_str") == "error":
                raise RuntimeError(json.dumps(status, ensure_ascii=False, indent=2))
        time.sleep(10)
    raise TimeoutError("ACE-Step music generation exceeded one hour")


if __name__ == "__main__":
    main()
