#!/usr/bin/env python3
"""Render the five Chinese-heaven image-to-video shots through local ComfyUI."""
import json
import argparse
import re
import shutil
import time
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
COMFY = Path("/nfs/FM/gongoubo/new_project/github/aigc/ComfyUI")
API = "http://127.0.0.1:8188"
WIDTH, HEIGHT, FRAMES, FPS = 1344, 768, 243, 24


def shots():
    text = (PROJECT / "视频生成提示词.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## 0([1-5]) (.+)$", text)
    result = []
    for i in range(1, len(parts), 3):
        number, title, body = int(parts[i]), parts[i + 1], parts[i + 2]
        prompt = body.split("\n## ", 1)[0].strip()
        result.append((number, title, prompt))
    if len(result) != 5:
        raise RuntimeError(f"expected five shot prompts, found {len(result)}")
    return result


def post(path, data=None):
    body = None if data is None else json.dumps(data, ensure_ascii=False).encode()
    request = urllib.request.Request(
        API + path, data=body,
        headers={"Content-Type": "application/json"} if body else {},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())


def graph(prompt, image_name, prefix, seed):
    return {
        "1": {"class_type": "ClipProjLoader", "inputs": {
            "clip_name": "qwen3vl_4b_int8_convrot.safetensors", "type": "krea2",
            "projection": "mmh3-4b-ClipProj-v3-mlp.safetensors", "device": "cuda:0", "mode": "streaming"}},
        "2": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "minimax_h3_ref2va_pruned_int8_convrot.safetensors", "weight_dtype": "default"}},
        "3": {"class_type": "MiniMaxH3SigmaShift", "inputs": {"model": ["2", 0], "shift_video": 12.0, "shift_audio": 3.0}},
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"}},
        "5": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
        "6": {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": {
            "clip": ["1", 0], "vae": ["4", 0], "audio_vae": ["5", 0], "prompt": prompt,
            "width": WIDTH, "height": HEIGHT, "length": FRAMES, "ref_image_size": "match",
            "ref_images.ref_image_0": ["16", 0]}},
        "7": {"class_type": "BasicGuider", "inputs": {"model": ["9", 0], "conditioning": ["6", 0]}},
        "8": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "9": {"class_type": "MiniMaxH3PDDAccApply", "inputs": {
            "model": ["3", 0], "pdd_file": "MiniMax-H3-Ref2VA-Acc-8Step.safetensors",
            "nfe": "8", "lora_strength": 1.0, "head_strength": 1.0,
            "on_off_grid": "error", "partition_check": "error"}},
        "10": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "11": {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["10", 0], "guider": ["7", 0], "sampler": ["8", 0],
            "sigmas": ["9", 1], "latent_image": ["6", 1]}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["4", 0]}},
        "13": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["11", 0], "vae": ["5", 0]}},
        "14": {"class_type": "CreateVideo", "inputs": {
            "images": ["12", 0], "audio": ["13", 0], "fps": float(FPS),
            "bit_depth": 8, "color_space": "sRGB", "codec": "none"}},
        "15": {"class_type": "SaveVideo", "inputs": {
            "video": ["14", 0], "filename_prefix": prefix,
            "format": "mp4", "format.codec": "h264"}},
        "16": {"class_type": "LoadImage", "inputs": {"image": image_name}},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", default="1,2,3,4,5", help="Comma-separated shot numbers")
    parser.add_argument("--port", type=int, default=8188)
    parser.add_argument("--tag", default="gpu0")
    args = parser.parse_args()
    global API
    API = f"http://127.0.0.1:{args.port}"
    log_path = PROJECT / "state" / "video_generation.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    (PROJECT / "视频" / "分段").mkdir(parents=True, exist_ok=True)
    comfy_input = COMFY / "input"
    comfy_input.mkdir(exist_ok=True)
    selected = {int(value) for value in args.shots.split(",") if value.strip()}
    for number, title, prompt in shots():
        if number not in selected:
            continue
        image_path = next((PROJECT / "资产").glob(f"0{number}_*.png"))
        image_name = f"chinese_heaven_shot_{number:02d}.png"
        shutil.copy2(image_path, comfy_input / image_name)
        prefix = f"video/chinese_heaven/{args.tag}_shot_{number:02d}"
        workflow = graph(prompt, image_name, prefix, 928110 + number)
        (PROJECT / "state" / f"shot_{number:02d}_api.json").write_text(
            json.dumps(workflow, ensure_ascii=False, indent=2), encoding="utf-8")
        queued = post("/prompt", {"prompt": workflow, "client_id": "chinese-heaven"})
        if "prompt_id" not in queued:
            raise RuntimeError(json.dumps(queued, ensure_ascii=False, indent=2))
        prompt_id = queued["prompt_id"]
        started = time.monotonic()
        line = f"{datetime.now().astimezone().isoformat(timespec='seconds')} queued shot {number}: {prompt_id}"
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        while time.monotonic() - started < 7200:
            history = post(f"/history/{prompt_id}")
            item = history.get(prompt_id)
            if item:
                status = item.get("status", {})
                if status.get("completed"):
                    outputs = item.get("outputs", {})
                    videos = []
                    for node_output in outputs.values():
                        videos.extend(node_output.get("videos", []))
                        videos.extend(item for item in node_output.get("images", []) if item.get("filename", "").endswith((".mp4", ".webm")))
                    if not videos:
                        raise RuntimeError(f"completed without a saved video: {outputs}")
                    video = videos[0]
                    source_video = COMFY / "output" / video.get("subfolder", "") / video["filename"]
                    target = PROJECT / "视频" / "分段" / f"0{number}_{title}.mp4"
                    shutil.copy2(source_video, target)
                    line = f"{datetime.now().astimezone().isoformat(timespec='seconds')} completed shot {number}: {target}"
                    print(line, flush=True)
                    with log_path.open("a", encoding="utf-8") as f:
                        f.write(line + "\n")
                    break
                if status.get("status_str") == "error":
                    raise RuntimeError(json.dumps(status, ensure_ascii=False, indent=2))
            time.sleep(10)
        else:
            raise TimeoutError(f"shot {number} exceeded two hours")


if __name__ == "__main__":
    main()
