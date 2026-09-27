#!/usr/bin/env python3
"""Make a white-figure / low-detail mask treatment like 素材/白模视频样例.png."""
from __future__ import annotations
import argparse
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "素材" / "7621879784973062134.mp4"
DEFAULT_OUTPUT = ROOT / "处理" / "深度黑白" / "7621879784973062134_白模样例风格.mp4"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    ap.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args(); args.output.parent.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(args.input)); fps=cap.get(cv2.CAP_PROP_FPS) or 30
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc=cv2.VideoWriter_fourcc(*'mp4v'); silent=args.output.with_suffix('.silent.mp4')
    writer=cv2.VideoWriter(str(silent), fourcc, fps, (w,h))
    # Fixed camera: temporal subtraction gives a stable silhouette of the two dancers.
    sub=cv2.createBackgroundSubtractorMOG2(history=180, varThreshold=20, detectShadows=False)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
    n=0
    while True:
        ok, frame=cap.read()
        if not ok: break
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fg=sub.apply(frame, learningRate=0.002 if n>20 else 0.05)
        fg=cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel)
        fg=cv2.morphologyEx(fg, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
        # Restrict to the central performance area; remove ceiling/text overlays.
        fg[:int(h*.34),:]=0; fg[int(h*.98):,:]=0
        # Keep only substantial connected components and softly expand body edges.
        count, labels, stats, _=cv2.connectedComponentsWithStats(fg,8)
        mask=np.zeros((h,w),np.uint8)
        for i in range(1,count):
            x,y,ww,hh,area=stats[i]
            # Reject floor/light changes and wide background structures; retain
            # the two human-sized components in the performance area.
            if 1800 < area < 90000 and hh > 80 and ww < int(w * .48) and y < int(h * .72):
                mask[labels==i]=255
        mask=cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)), 1)
        # Low-detail grayscale background, then white mannequin figures.
        bg=cv2.GaussianBlur(gray,(0,0),1.8)
        bg=(np.floor(bg/32)*32).clip(0,224).astype(np.uint8)
        out=cv2.cvtColor(bg,cv2.COLOR_GRAY2BGR)
        out[mask>0]=(245,245,245)
        writer.write(out); n+=1
    cap.release(); writer.release()
    # Add the original audio back.
    import subprocess
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(silent),'-i',str(args.input),'-map','0:v:0','-map','1:a?','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(args.output)],check=True)
    silent.unlink(missing_ok=True)
    print(args.output)

if __name__=='__main__': main()
