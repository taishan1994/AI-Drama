"""Build target-stage motion references from depth silhouettes.

Foreground people are extracted from the source video with COCO DeepLabV3;
the stage in the H3 video reference is replaced with the target moonlit stage
so the source studio cannot leak into the generated frames.
"""
from pathlib import Path
import cv2
import numpy as np
import torch
from PIL import Image, ImageOps
from torchvision.models.segmentation import deeplabv3_resnet50, DeepLabV3_ResNet50_Weights

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "素材/7621879784973062134.mp4"
DEPTH = PROJECT / "处理/深度图/7621879784973062134_depth.mp4"
STAGE = PROJECT / "资产/stage.png"
OUT = PROJECT / "处理/动作参考_目标舞台.mp4"
PREVIEW = PROJECT / "检查/动作参考_目标舞台_contact.png"
WIDTH, HEIGHT, FPS = 720, 1280, 24

def get_frame(cap, frame_index):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
    ok, frame = cap.read()
    if not ok:
        return None
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def main():
    device = torch.device("cuda:1" if torch.cuda.is_available() and torch.cuda.device_count() > 1 else "cuda:0" if torch.cuda.is_available() else "cpu")
    weights = DeepLabV3_ResNet50_Weights.DEFAULT
    model = deeplabv3_resnet50(weights=weights).to(device).eval()
    person_id = weights.meta["categories"].index("person")
    preprocess = weights.transforms()
    stage = ImageOps.fit(Image.open(STAGE).convert("RGB"), (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
    stage = np.asarray(stage).copy()
    src = cv2.VideoCapture(str(SOURCE))
    dep = cv2.VideoCapture(str(DEPTH))
    src_fps = src.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(round(src.get(cv2.CAP_PROP_FRAME_COUNT) / src_fps * FPS))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(OUT), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (WIDTH, HEIGHT))
    prev_centers = None
    snapshots = []
    for j in range(total):
        t = j / FPS
        rgb = get_frame(src, round(t * src_fps))
        dep_rgb = get_frame(dep, round(t * 30))
        if rgb is None or dep_rgb is None:
            break
        inp = preprocess(Image.fromarray(rgb)).unsqueeze(0).to(device)
        with torch.inference_mode():
            logits = model(inp)["out"]
            probs = torch.softmax(logits, 1)[0, person_id].detach().cpu().numpy()
        prob = cv2.resize(probs, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
        mask = (prob > 0.34).astype(np.uint8)
        # Keep only the performance area; this excludes ceiling text, lights,
        # and the floor while retaining the skirts and raised fans.
        roi = np.zeros_like(mask)
        roi[360:1100, 35:690] = 1
        mask *= roi
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, labels, stats, cents = cv2.connectedComponentsWithStats(mask, 8)
        comps = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= 5000]
        comps.sort(key=lambda i: stats[i, cv2.CC_STAT_AREA], reverse=True)
        comps = comps[:2]
        if len(comps) == 2:
            centers = [cents[k].astype(float) for k in comps]
            if prev_centers is None:
                order = np.argsort([c[0] for c in centers])
                comps = [comps[x] for x in order]
                centers = [centers[x] for x in order]
            else:
                direct = np.linalg.norm(centers[0] - prev_centers[0]) + np.linalg.norm(centers[1] - prev_centers[1])
                crossed = np.linalg.norm(centers[1] - prev_centers[0]) + np.linalg.norm(centers[0] - prev_centers[1])
                if crossed < direct:
                    comps.reverse(); centers.reverse()
            prev_centers = centers
        elif len(comps) == 1:
            # During a close crossing the masks can merge; split the merged
            # silhouette down the midpoint of the two tracked dancers.
            if prev_centers is not None:
                idx = comps[0]
                ys, xs = np.where(labels == idx)
                mid = (prev_centers[0][0] + prev_centers[1][0]) / 2
                halves = [(xs <= mid), (xs > mid)]
                comps_masks = [np.zeros_like(mask, dtype=np.float32) for _ in range(2)]
                for k, keep in enumerate(halves):
                    comps_masks[k][ys[keep], xs[keep]] = 1.0
            else:
                comps_masks = [np.zeros_like(mask, dtype=np.float32), np.zeros_like(mask, dtype=np.float32)]
                ys, xs = np.where(labels == comps[0])
                mid = np.median(xs)
                comps_masks[0][ys[xs <= mid], xs[xs <= mid]] = 1.0
                comps_masks[1][ys[xs > mid], xs[xs > mid]] = 1.0
        else:
            comps_masks = [np.zeros_like(mask, dtype=np.float32), np.zeros_like(mask, dtype=np.float32)]
        if len(comps) == 2:
            comps_masks = [(labels == idx).astype(np.float32) for idx in comps]
        depth = cv2.cvtColor(cv2.resize(dep_rgb, (WIDTH, HEIGHT)), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        canvas = stage.copy().astype(np.float32)
        colors = [(68, 139, 143), (166, 57, 55)]
        for matte, color in zip(comps_masks, colors):
            matte = cv2.GaussianBlur(matte, (0, 0), 1.25)
            if float(matte.max()) < 0.05:
                continue
            shade = 0.72 + 0.28 * depth
            fill = np.array(color, np.float32)[None, None, :] * shade[:, :, None]
            alpha = (matte * 0.94)[:, :, None]
            canvas = canvas * (1 - alpha) + fill * alpha
        out = np.clip(canvas, 0, 255).astype(np.uint8)
        writer.write(cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
        if j in {0, 24, 48, 72, 96, 120, 240, 360, 480, 600}:
            snapshots.append(Image.fromarray(out).resize((180, 320)))
        if j % 120 == 0:
            print(f"frames {j}/{total}", flush=True)
    src.release(); dep.release(); writer.release()
    if snapshots:
        cols = 5; rows = (len(snapshots) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 180, rows * 320))
        for i, im in enumerate(snapshots): sheet.paste(im, ((i % cols) * 180, (i // cols) * 320))
        sheet.save(PREVIEW)
    print(OUT, flush=True)

if __name__ == "__main__": main()
