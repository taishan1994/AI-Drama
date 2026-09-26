"""Relative depth video: near white, far black; no luminance thresholding."""
from pathlib import Path
import argparse, subprocess, json
import cv2
import numpy as np
import torch
from transformers import AutoImageProcessor, AutoModelForDepthEstimation

ROOT = Path(__file__).resolve().parents[4]
MODEL = ROOT / 'ComfyUI/models/depth/Depth-Anything-V2-Small-hf'

def run(source, output, device='cuda:1', preview=False, model_path=MODEL):
    torch.set_num_threads(8)
    source, output = Path(source), Path(output)
    if source.resolve() == output.resolve():
        raise ValueError('Output must not overwrite source')
    output.parent.mkdir(parents=True, exist_ok=True)
    processor = AutoImageProcessor.from_pretrained(str(model_path), local_files_only=True)
    model = AutoModelForDepthEstimation.from_pretrained(str(model_path), local_files_only=True).to(device).eval()
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError(f'Cannot open {source}')
    w,h = (int(cap.get(k)) for k in (cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    def predict(frame):
        inputs = processor(images=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), return_tensors='pt').to(device)
        with torch.inference_mode():
            depth = model(**inputs).predicted_depth
            depth = torch.nn.functional.interpolate(depth[:,None],(h,w),mode='bilinear',align_corners=False)[0,0]
        return depth.cpu().numpy()
    # One robust scale over the whole clip avoids per-frame brightness pumping.
    lows, highs, samples = [], [], []
    for idx in np.linspace(0,total-1,12,dtype=int):
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(idx)); ok,frame = cap.read()
        if not ok: continue
        d = predict(frame); lows.append(np.percentile(d,2)); highs.append(np.percentile(d,98)); samples.append((idx,frame,d))
    lo,hi = float(np.median(lows)),float(np.median(highs))
    def render(d):
        # Compress the near-depth range to reproduce the sample's bright figures.
        # This maps estimated distance, never source clothing/lighting brightness.
        x = np.clip((d-lo)/max(hi-lo,1e-6)*3.0,0,1)**0.7
        return (cv2.bilateralFilter(x.astype(np.float32),5,.08,3)*255).astype(np.uint8)
    panels=[]
    for idx,frame,d in samples[::3]:
        dep = cv2.cvtColor(render(d),cv2.COLOR_GRAY2BGR)
        panels.append(cv2.resize(np.hstack([frame,dep]),(576,512)))
    cv2.imwrite(str(output.with_suffix('.preview.jpg')),np.vstack(panels))
    if preview: cap.release(); return
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    temp=output.with_name(output.stem+'.partial.mp4')
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','gray','-s',f'{w}x{h}','-r',str(fps),'-i','pipe:0','-i',str(source),'-map','0:v','-map','1:a?','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(temp)]
    encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    count=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok: break
            encoder.stdin.write(render(predict(frame)).tobytes()); count+=1
            if count%60==0: print(f'{count}/{total}',flush=True)
    finally:
        cap.release(); encoder.stdin.close()
    if encoder.wait()!=0 or count!=total: raise RuntimeError(f'Incomplete encode {count}/{total}')
    temp.replace(output)
    output.with_suffix('.json').write_text(json.dumps(dict(model=str(model_path),source=str(source),frames=count,fps=fps,depth_range=[lo,hi],gain=3.0,gamma=0.7,near='white',far='black'),indent=2))
    print(str(output),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--model',default=str(MODEL))
    p.add_argument('--device',default='cuda:1')
    p.add_argument('--preview',action='store_true')
    a=p.parse_args();run(a.input,a.output,a.device,a.preview,a.model)
