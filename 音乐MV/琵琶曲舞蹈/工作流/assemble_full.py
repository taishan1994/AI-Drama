"""Join six H3 clips without shifting music; add short, beat-safe dip transitions."""
from pathlib import Path
import json, subprocess, cv2, numpy as np

P = Path(__file__).resolve().parents[1]
SEG_DIR = P / "视频/分段"
OUT_DIR = P / "视频"
FPS, W, H = 24, 768, 1344
N_PER = 124
N_TOTAL = 668

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,avg_frame_rate,codec_name,sample_rate,channels", "-of", "json", str(path)], check=True, capture_output=True, text=True)
    return json.loads(r.stdout)

def decode(path):
    cap = cv2.VideoCapture(str(path)); arr=[]
    while True:
        ok, frame = cap.read()
        if not ok: break
        if frame.shape[1] != W or frame.shape[0] != H:
            frame = cv2.resize(frame, (W,H), interpolation=cv2.INTER_LANCZOS4)
        arr.append(frame)
    cap.release()
    return arr

def main():
    chunks=[]
    for i in range(6):
        f=SEG_DIR/f"段{i+1:02d}_待检查.mp4"
        if not f.exists(): raise SystemExit(f"Missing segment: {f}")
        frames=decode(f)
        required=N_PER if i<5 else N_TOTAL-N_PER*5
        if len(frames)<required:
            raise SystemExit(f"Segment {i+1} has only {len(frames)} frames; needs {required}")
        chunks.append(frames[:required])
    # Prefer a frame-matched cut because each segment is conditioned on the
    # preceding segment's true last frame. If the seam differs too much, use a
    # four-frame dip through dark instead of overlaying two chair silhouettes.
    out_frames=[]
    transition_records=[]
    for i, chunk in enumerate(chunks):
        if i:
            prev=chunks[i-1]
            seam_delta=float(np.abs(prev[-1].astype(np.float32)-chunk[0].astype(np.float32)).mean())
            if seam_delta <= 10.0:
                out_frames.extend(chunk)
                style="pose-matched cut; adjacent frames closely match"
                transition_frames=0
            else:
                transition=[(prev[-2].astype(np.float32)*0.72).astype(np.uint8),
                            (prev[-1].astype(np.float32)*0.28).astype(np.uint8),
                            (chunk[0].astype(np.float32)*0.28).astype(np.uint8),
                            (chunk[1].astype(np.float32)*0.72).astype(np.uint8)]
                out_frames[-2:]=transition[:2]
                out_frames.extend(transition[2:])
                out_frames.extend(chunk[2:])
                style="four-frame dip-to-dark; no image overlap"
                transition_frames=4
            transition_records.append({"at_seconds":round(i*N_PER/FPS,3),"duration_frames":transition_frames,"style":style,"mean_abs_seam_delta_0_255":round(seam_delta,3)})
        else:
            out_frames.extend(chunk)
    if len(out_frames)!=N_TOTAL:
        raise SystemExit(f"Assembly produced {len(out_frames)} frames, expected {N_TOTAL}")
    tmp_video=OUT_DIR/"琵琶夜宴_拼接无音频.mp4"
    writer=cv2.VideoWriter(str(tmp_video),cv2.VideoWriter_fourcc(*"mp4v"),FPS,(W,H))
    for fr in out_frames: writer.write(fr)
    writer.release()
    source_video=P/"素材/7621879784973062134.mp4"
    source_audio=P/"素材/原始音频.m4a"
    out=OUT_DIR/"琵琶夜宴_双人古装舞_原曲_完整.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(tmp_video),"-i",str(source_audio),"-map","0:v:0","-map","1:a:0","-t",f"{N_TOTAL/FPS:.9f}","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",str(out)],check=True)
    tmp_video.unlink(missing_ok=True)
    probe_data = probe(out)
    audio_rows = [s for s in probe_data.get("streams", []) if s.get("sample_rate")]
    report={
        "output":str(out),"segments":6,"video_frames":N_TOTAL,"fps":FPS,
        "resolution":"768x1344","expected_video_duration_seconds":round(N_TOTAL/FPS,6),
        "audio_source":str(source_audio),"audio_policy":"use the standalone original audio file; preserve source timeline",
        "transitions":transition_records,
        "segment_files":[str(SEG_DIR/f"段{i+1:02d}_待检查.mp4") for i in range(6)],
        "ffprobe":probe_data,
        "audio_streams":audio_rows
    }
    beat_path=P/"工作流/原曲节拍与转场点.json"
    if beat_path.exists():
        beat_data=json.loads(beat_path.read_text())
        report["audio_beat_analysis"]={"method":"short-time spectral flux onset peaks","nearest_strong_onsets":beat_data.get("nearest_strong_onsets",[])}
    (P/"工作流/完整成片技术报告.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    # Compare the final muxed soundtrack with the original source soundtrack.
    source_wav=OUT_DIR/"_qc_source_8k.wav"; final_wav=OUT_DIR/"_qc_final_8k.wav"
    for input_path, output_path in [(source_audio,source_wav),(out,final_wav)]:
        subprocess.run(["ffmpeg","-y","-v","error","-i",str(input_path),"-vn","-ac","1","-ar","8000","-c:a","pcm_s16le",str(output_path)],check=True)
    import wave
    def read_mono(path):
        with wave.open(str(path),"rb") as w:
            return np.frombuffer(w.readframes(w.getnframes()),dtype="<i2").astype(np.float32)
    src=read_mono(source_wav); final=read_mono(final_wav); n=min(len(src),len(final)); src=src[:n]; final=final[:n]
    src-=src.mean(); final-=final.mean()
    fft_size=1 << (2*n-1).bit_length()
    corr=np.fft.irfft(np.fft.rfft(final,fft_size)*np.conj(np.fft.rfft(src,fft_size)),fft_size)
    lag_limit=4000
    near=np.concatenate((corr[-lag_limit:],corr[:lag_limit+1]))
    lags=np.arange(-lag_limit,lag_limit+1)
    best_lag=int(lags[int(np.argmax(near))])
    audio_alignment={"sample_rate_hz":8000,"compared_duration_seconds":round(n/8000,4),
                     "best_lag_ms":round(best_lag*1000/8000,3),
                     "zero_lag_pearson_correlation":round(float(np.corrcoef(src,final)[0,1]),6)}
    report["audio_alignment_check"]=audio_alignment
    (P/"工作流/完整成片技术报告.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    source_wav.unlink(missing_ok=True); final_wav.unlink(missing_ok=True)
    print(out)

if __name__=="__main__": main()
