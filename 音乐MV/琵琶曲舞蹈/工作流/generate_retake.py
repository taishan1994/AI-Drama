"""Generate retake clips one at a time for user review."""
from pathlib import Path
import argparse, json, shutil, subprocess, time, urllib.request
import cv2

P = Path(__file__).resolve().parents[1]
COMFY = P.parents[2] / "ComfyUI"
INPUT = COMFY / "input"
API = "http://127.0.0.1:8188"
BASE = P / "工作流/H3_5秒输出_15秒参考_API.json"
GUIDE = P / "处理/动作参考_目标舞台_v2.mp4"
MASTER_AUDIO = P / "素材/原始音频.m4a"
KEYFRAME0 = INPUT / "pipa_duet_keyframe_v3.png"
FPS, WIDTH, HEIGHT = 24, 768, 1344
CHUNK = 124
FINAL_FRAMES = 56
OUT_DIR = P / "视频/重制分段"

def frames_for(i): return FINAL_FRAMES if i == 5 else CHUNK

def request(path, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(API + path, data=body, headers={"Content-Type":"application/json"} if body else {})
    with urllib.request.urlopen(req, timeout=120) as response: return json.load(response)

def prepare(i):
    name=f"pipa_retake_{i+1:02d}"
    vp=INPUT/f"{name}_motion.mp4"; ap=INPUT/f"{name}_audio.wav"
    cap=cv2.VideoCapture(str(GUIDE)); cap.set(cv2.CAP_PROP_POS_FRAMES,i*CHUNK)
    fs=[]
    for _ in range(frames_for(i)):
        ok,f=cap.read()
        if not ok: break
        fs.append(f)
    cap.release()
    if not fs: raise RuntimeError(f"no guide frames for segment {i+1}")
    while len(fs)<frames_for(i): fs.append(fs[-1].copy())
    h,w=fs[0].shape[:2]
    wr=cv2.VideoWriter(str(vp),cv2.VideoWriter_fourcc(*"mp4v"),FPS,(w,h))
    for f in fs: wr.write(f)
    wr.release()
    start=i*CHUNK/FPS; duration=frames_for(i)/FPS
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{start:.9f}","-i",str(MASTER_AUDIO),"-t",f"{duration:.9f}","-af","apad=pad_dur=5","-ar","32000","-ac","2","-c:a","pcm_s16le",str(ap)],check=True)
    return vp.name,ap.name

def make_prompt(i):
    start=i*CHUNK/FPS; end=min(27.834,start+frames_for(i)/FPS)
    return f"""subject_definitions:
<Subject 1> Qingyi is the adult woman in teal Hanfu in <Picture 1>, with the oval face, high bun and jade pin. She corresponds permanently to the lighter-costume dancer tinted teal in <Video 1>. Her face, hair, and costume stay teal through every turn, crossing, and overlap.
<Subject 2> Hongyi is the distinct adult woman in vermilion Hanfu in <Picture 1>, with the rounder face and gold hair ornaments. She corresponds permanently to the darker-costume dancer tinted vermilion in <Video 1>. Her face, hair, and costume stay vermilion through every turn, crossing, and overlap.
<Picture 1> The exact opening full-scene composition: these same two women in a flowing counterbalance around exactly one chair placed slightly left of center and low in frame. Preserve the chair's location and the moonlit pavilion.
<Audio 1> Original music excerpt at source time {start:.3f}-{end:.3f} seconds, paired to <Video 1> and used for precise rhythm.
<Video 1> High-detail, color-coded motion guide on the final stage. It preserves the source dancers' sleeve, skirt, torso and limb motion. Teal labels always mark Qingyi; vermilion labels always mark Hongyi. Follow their motion timing and spatial paths, never exchange identities or costume colors. Do not copy the guide's simplified tint as costume texture.

summary:
Photorealistic 9:16 Chinese historical fan dance, retake segment {i+1} of 6, source time {start:.3f}-{end:.3f}s. Natural, expressive continuous movement, stable two-woman identities, source-matched chair placement and original music.

retention_analysis:
Exactly two adult women and one stationary carved wooden chair. Qingyi remains teal with her jade pin and oval face; Hongyi remains vermilion with gold ornaments and a rounder face. Identity is attached to each dancer, not screen side: crossing, turning, touching, or temporary occlusion never changes faces, hairstyles, or dress colors. In overlap, preserve clear front/back occlusion and let one body pass behind the other; never blend or exchange garments. Chair stays at the same slightly-left, low position shown in <Picture 1> and <Video 1>. Keep the same moonlit pavilion set, curtains, lake, mountains, and reflective wooden floor in every frame. No extra chairs, furniture, people, text, studio background, or scene cuts.

detailed_description:
Continue directly from the opening pose in <Picture 1>. Follow <Video 1> from {start:.3f} to {end:.3f}s: reproduce the complete weight shifts, turns, traveling steps, sleeve/fan arcs, torso bends, partner counterbalances, chair approaches, and footwork in order and on the original beats. Make each move flow through its transition with visible weight transfer, relaxed wrists, curved arms, natural skirt and sleeve follow-through, and changing but balanced poses; avoid held mannequin poses, stiff straight arms, robotic timing, and abrupt pose jumps. Keep both dancers grounded, full-body, and spatially distinct. Keep the camera locked in the full-stage portrait frame. Use the original music only, no dialogue or added sounds."""

def make_graph(i,keyframe,vname,aname):
    g=json.loads(BASE.read_text())
    g["6"]["inputs"].update({"width":WIDTH,"height":HEIGHT,"length":frames_for(i),"prompt":make_prompt(i),"ref_images.ref_image_0":["18",0],"ref_videos.ref_video_0":["21",0],"ref_video_audios.ref_video_audio_0":["22",0]})
    for k in ("ref_images.ref_image_1","ref_images.ref_image_2"): g["6"]["inputs"].pop(k,None)
    g["18"]["inputs"]["image"]=keyframe.name
    g["20"]["inputs"]["file"]=vname; g["22"]["inputs"]["audio"]=aname; g["23"]["inputs"]["audio"]=aname
    g["15"]["inputs"]["filename_prefix"]=f"video/pipa_duet/retake_seg{i+1:02d}"
    g["10"]["inputs"]["noise_seed"]=76219701+i
    return g

def get_output(hist):
    for x in hist.get("outputs",{}).get("15",{}).get("images",[]):
        if isinstance(x,dict) and x.get("filename","").endswith(".mp4"): return x
    return None

def run(i):
    OUT_DIR.mkdir(parents=True,exist_ok=True)
    keyframe=KEYFRAME0 if i==0 else INPUT/f"pipa_retake_keyframe_after_{i:02d}.png"
    vname,aname=prepare(i); graph=make_graph(i,keyframe,vname,aname)
    wf=P/"工作流"/f"H3_重制第{i+1:02d}段_API.json"; wf.write_text(json.dumps(graph,ensure_ascii=False,indent=2))
    queued=request("/prompt",{"prompt":graph,"client_id":"pipa-duet-retake"}); pid=queued["prompt_id"]
    (P/"工作流"/f"H3_重制第{i+1:02d}段任务.json").write_text(json.dumps({"prompt_id":pid,"segment":i+1,"start_time":i*CHUNK/FPS,"frames":frames_for(i)},ensure_ascii=False,indent=2))
    print(f"queued retake segment {i+1}, prompt {pid}",flush=True)
    while True:
        hist=request("/history/"+pid).get(pid)
        if hist:
            status=hist.get("status",{})
            if status.get("status_str")=="error":
                (P/"工作流"/f"H3_重制第{i+1:02d}段错误.json").write_text(json.dumps(hist,ensure_ascii=False,indent=2)); raise RuntimeError(status)
            if status.get("completed"):
                (P/"工作流"/f"H3_重制第{i+1:02d}段历史.json").write_text(json.dumps(hist,ensure_ascii=False,indent=2))
                item=get_output(hist)
                if not item: raise RuntimeError("completed but no mp4 output")
                src=COMFY/"output"/item.get("subfolder","")/item["filename"]
                dst=OUT_DIR/f"重制段{i+1:02d}_待验收.mp4"; shutil.copy2(src,dst)
                if i<5:
                    cap=cv2.VideoCapture(str(dst)); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,n-1)); ok,fr=cap.read(); cap.release()
                    if not ok: raise RuntimeError("cannot extract final frame")
                    cv2.imwrite(str(INPUT/f"pipa_retake_keyframe_after_{i+1:02d}.png"),fr)
                print(f"saved {dst}",flush=True); return
        time.sleep(8)

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--segment",type=int,required=True,choices=range(1,7)); a=parser.parse_args(); run(a.segment-1)
