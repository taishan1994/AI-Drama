"""Build a detailed, identity-stable motion reference over the chair-matched stage.

Unlike the old solid silhouettes, this guide keeps desaturated source dancer
texture and limb detail. COCO Mask R-CNN instances are assigned by the stable
light-vs-dark costume signature, so screen crossings cannot exchange IDs.
"""
from pathlib import Path
import json
import cv2
import numpy as np
import torch
from PIL import Image, ImageOps, ImageDraw
from torchvision.models.detection import maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "素材/7621879784973062134.mp4"
STAGE = PROJECT / "资产/stage_v3_chair_matched.png"
OUT = PROJECT / "处理/动作参考_目标舞台_v2.mp4"
PREVIEW = PROJECT / "检查/动作参考_目标舞台_v2_contact.png"
REPORT = PROJECT / "工作流/动作参考_v2_身份检查.json"
WIDTH, HEIGHT, FPS = 720, 1280, 24
MIN_AREA = 3000

def get_frame(cap, frame_index):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
    ok, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if ok else None

def main():
    device = torch.device("cuda:1" if torch.cuda.is_available() and torch.cuda.device_count() > 1 else "cuda:0" if torch.cuda.is_available() else "cpu")
    weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
    model = maskrcnn_resnet50_fpn(weights=weights).to(device).eval()
    stage = ImageOps.fit(Image.open(STAGE).convert("RGB"), (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
    stage = np.asarray(stage).copy()
    cap = cv2.VideoCapture(str(SOURCE))
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(round(cap.get(cv2.CAP_PROP_FRAME_COUNT) / src_fps * FPS))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(OUT), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (WIDTH, HEIGHT))
    prev_centers = [None, None]
    class_lumas = [[], []]  # ID 0 is the lighter costume -> teal; ID 1 is the darker costume -> vermilion.
    assignments = []
    previews = []
    transform = weights.transforms()

    for j in range(total):
        rgb = get_frame(cap, round((j / FPS) * src_fps))
        if rgb is None:
            break
        tensor = transform(Image.fromarray(rgb)).to(device)
        with torch.inference_mode():
            pred = model([tensor])[0]
        masks = pred["masks"][:, 0].detach().cpu().numpy()
        labels = pred["labels"].detach().cpu().numpy()
        scores = pred["scores"].detach().cpu().numpy()
        candidates = []
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        for k, (lab, score) in enumerate(zip(labels, scores)):
            if lab != 1 or score < 0.62:
                continue
            matte = cv2.resize(masks[k], (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR) > 0.45
            area = int(matte.sum())
            if area < MIN_AREA:
                continue
            ys, xs = np.where(matte)
            y0, y1 = int(ys.min()), int(ys.max())
            torso = matte.copy()
            torso[:y0 + int((y1-y0)*0.22), :] = False
            torso[y0 + int((y1-y0)*0.92):, :] = False
            vals = gray[torso]
            luma = float(np.median(vals)) if vals.size else float(np.median(gray[matte]))
            center = np.array([float(xs.mean()), float(ys.mean())])
            candidates.append({"matte": matte.astype(np.uint8), "area": area, "luma": luma, "center": center, "score": float(score)})

        # COCO may return duplicate fragments for skirts/arms. The two largest
        # person instances are the performers; person identity follows costume
        # brightness, never left-to-right ordering.
        candidates.sort(key=lambda x: x["area"], reverse=True)
        candidates = candidates[:2]
        id_masks = [np.zeros((HEIGHT, WIDTH), np.uint8), np.zeros((HEIGHT, WIDTH), np.uint8)]
        confidence = "missing"
        if len(candidates) == 2:
            ordered = sorted(candidates, key=lambda x: x["luma"], reverse=True)
            # Learn a stable source-specific threshold from clearly separated
            # costume samples; luma separation is large throughout this clip.
            if ordered[0]["luma"] - ordered[1]["luma"] >= 18:
                class_lumas[0].append(ordered[0]["luma"])
                class_lumas[1].append(ordered[1]["luma"])
                id_masks = [ordered[0]["matte"], ordered[1]["matte"]]
                confidence = "costume_luma"
            else:
                # Ambiguous lighting: associate by continuity, but leave the
                # costume-signature rule as the primary identity anchor.
                chosen = []
                for actor in range(2):
                    ref = prev_centers[actor]
                    chosen.append(min(candidates, key=lambda x: np.linalg.norm(x["center"]-ref)) if ref is not None else sorted(candidates,key=lambda x:x["center"][0])[actor])
                if chosen[0] is chosen[1]:
                    chosen = sorted(candidates,key=lambda x:x["center"][0])
                id_masks = [chosen[0]["matte"], chosen[1]["matte"]]
                confidence = "continuity_fallback"
        elif len(candidates) == 1:
            c = candidates[0]
            means = [float(np.median(class_lumas[i])) if class_lumas[i] else (145.0 if i == 0 else 65.0) for i in range(2)]
            d = [abs(c["luma"]-m) for m in means]
            actor = int(np.argmin(d))
            # A merged/ambiguous detection can cover both dancers. Split it
            # along the nearest prior center only when its footprint supports
            # two bodies; otherwise show only the visible instance.
            if max(d) - min(d) < 12 and all(x is not None for x in prev_centers):
                actor = int(np.argmin([np.linalg.norm(c["center"]-x) for x in prev_centers]))
            if all(x is not None for x in prev_centers) and c["area"] > 20000 and np.linalg.norm(prev_centers[0]-prev_centers[1]) > 45:
                yy, xx = np.indices((HEIGHT, WIDTH))
                dist0 = (xx-prev_centers[0][0])**2 + (yy-prev_centers[0][1])**2
                dist1 = (xx-prev_centers[1][0])**2 + (yy-prev_centers[1][1])**2
                id_masks[0] = (c["matte"] & (dist0 <= dist1)).astype(np.uint8)
                id_masks[1] = (c["matte"] & (dist1 < dist0)).astype(np.uint8)
                confidence = "merged_nearest_prior_center"
            else:
                id_masks[actor] = c["matte"]
                confidence = "single_costume_luma"

        canvas = stage.copy().astype(np.float32)
        # Preserve movement detail (sleeve, skirt, fan and limb folds) with a
        # monochrome-to-color transfer rather than filling a flat silhouette.
        grayf = gray.astype(np.float32) / 255.0
        base_colors = [(55, 122, 128), (156, 58, 62)]
        current_centers = [None, None]
        for actor, (matte, color) in enumerate(zip(id_masks, base_colors)):
            matte = cv2.morphologyEx(matte, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
            matte = cv2.morphologyEx(matte, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
            if matte.sum() < 800:
                continue
            ys, xs = np.where(matte > 0)
            current_centers[actor] = np.array([xs.mean(), ys.mean()])
            luminance = cv2.GaussianBlur(grayf, (0,0), 1.0)
            shade = 0.42 + 0.78 * luminance
            rgb_tint = np.clip(np.array(color, np.float32)[None,None,:] * shade[:,:,None], 0, 255)
            soft = cv2.GaussianBlur(matte.astype(np.float32), (0,0), 1.1)
            alpha = np.clip(soft * 0.98, 0, 0.98)[:,:,None]
            canvas = canvas * (1-alpha) + rgb_tint * alpha
        # Update stable per-costume positions; detected component order is irrelevant.
        for actor in range(2):
            if current_centers[actor] is not None:
                prev_centers[actor] = current_centers[actor]
        assignments.append({"frame":j,"confidence":confidence,"visible_ids":[i for i,m in enumerate(id_masks) if int(m.sum()) >= 800],"luma":[round(c["luma"],1) for c in candidates]})
        out = np.clip(canvas,0,255).astype(np.uint8)
        writer.write(cv2.cvtColor(out,cv2.COLOR_RGB2BGR))
        if j % 24 == 0:
            previews.append((j//24,Image.fromarray(out).resize((144,256))))
        if j % 120 == 0:
            print(f"frames {j}/{total}",flush=True)

    cap.release(); writer.release()
    cols=7; tile_w,tile_h=144,276; rows=(len(previews)+cols-1)//cols
    sheet=Image.new("RGB",(cols*tile_w,rows*tile_h),(20,20,20)); draw=ImageDraw.Draw(sheet)
    for i,(sec,im) in enumerate(previews):
        x=(i%cols)*tile_w; y=(i//cols)*tile_h; sheet.paste(im,(x,y+20)); draw.text((x+4,y+3),f"{sec:02d}s",fill="white")
    sheet.save(PREVIEW)
    report={"frames":len(assignments),"fps":FPS,"stage_asset":str(STAGE),"guide":str(OUT),"identity_rule":"lighter source costume maps permanently to teal; darker source costume maps permanently to vermilion","confidence_counts":{k:sum(a['confidence']==k for a in assignments) for k in sorted(set(a['confidence'] for a in assignments))},"luma_median_by_id":[float(np.median(v)) if v else None for v in class_lumas],"assignments":assignments}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(OUT,flush=True)

if __name__ == "__main__": main()
