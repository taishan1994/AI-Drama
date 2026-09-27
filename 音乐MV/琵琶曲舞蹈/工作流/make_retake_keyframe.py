"""Place the two identity-stable characters onto the exact chair-matched plate."""
from pathlib import Path
import cv2
import numpy as np
import torch
from PIL import Image, ImageOps
from torchvision.models.detection import maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights
from torchvision.models.segmentation import deeplabv3_resnet50, DeepLabV3_ResNet50_Weights

P=Path(__file__).resolve().parents[1]
SOURCE=P/"资产/双人舞首帧_v3_模型图.png"
STAGE=P/"资产/stage_v3_chair_matched.png"
OUT=P/"资产/双人舞首帧_v3_最终.png"
COMFY= P.parents[2]/"ComfyUI/input/pipa_duet_keyframe_v3.png"
W,H=768,1344

def main():
    dev=torch.device("cuda:1" if torch.cuda.is_available() and torch.cuda.device_count()>1 else "cuda:0" if torch.cuda.is_available() else "cpu")
    weights=MaskRCNN_ResNet50_FPN_Weights.DEFAULT
    model=maskrcnn_resnet50_fpn(weights=weights).to(dev).eval()
    seg_weights=DeepLabV3_ResNet50_Weights.DEFAULT
    segmenter=deeplabv3_resnet50(weights=seg_weights).to(dev).eval()
    src=ImageOps.fit(Image.open(SOURCE).convert("RGB"),(W,H),method=Image.Resampling.LANCZOS)
    bg=ImageOps.fit(Image.open(STAGE).convert("RGB"),(W,H),method=Image.Resampling.LANCZOS)
    with torch.inference_mode(): pred=model([weights.transforms()(src).to(dev)])[0]
    labels=pred["labels"].cpu().numpy(); scores=pred["scores"].cpu().numpy(); masks=pred["masks"][:,0].cpu().numpy()
    people=[]
    for i,(lab,score) in enumerate(zip(labels,scores)):
        if lab!=1 or score<.65: continue
        m=cv2.resize(masks[i],(W,H),interpolation=cv2.INTER_LINEAR)
        b=m>.38
        if int(b.sum())<12000: continue
        ys,xs=np.where(b); people.append((int(b.sum()),float(xs.mean()),m))
    people.sort(reverse=True,key=lambda x:x[0]); people=people[:2]
    if len(people)!=2: raise RuntimeError(f"expected two person instances, got {len(people)}")
    people.sort(key=lambda x:x[1]) # teal left, vermilion right in the opening composition.
    with torch.inference_mode():
        seg=segmenter(seg_weights.transforms()(src).unsqueeze(0).to(dev))["out"].softmax(1)[0,seg_weights.meta["categories"].index("person")].cpu().numpy()
    person_prob=cv2.resize(seg,(W,H),interpolation=cv2.INTER_LINEAR)
    dets=[]
    for _,_,prob in people:
        det=prob>.38
        dist=cv2.distanceTransform((~det).astype(np.uint8),cv2.DIST_L2,5)
        yy,xx=np.where(det); x0,x1=xx.min(),xx.max(); y0,y1=yy.min(),yy.max()
        pad_x=int((x1-x0)*.10); pad_y=int((y1-y0)*.22)
        roi=np.zeros((H,W),bool); roi[max(0,y0-pad_y):min(H,y1+int(pad_y*.35)),max(0,x0-pad_x):min(W,x1+pad_x)]=True
        dets.append((det,dist,roi))
    canvas=np.asarray(bg).astype(np.float32)
    d0,d1=dets
    for det,dist,roi in dets:
        other=d1[1] if det is d0[0] else d0[1]
        matte=det | (roi & (person_prob>.22) & (dist<=other))
        matte=cv2.morphologyEx(matte.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
        alpha=cv2.GaussianBlur(matte.astype(np.float32),(0,0),1.0)*.995
        fg=np.asarray(src).astype(np.float32)
        canvas=fg*alpha[:,:,None]+canvas*(1-alpha[:,:,None])
    result=Image.fromarray(np.clip(canvas,0,255).astype(np.uint8))
    result.save(OUT)
    COMFY.parent.mkdir(parents=True,exist_ok=True); result.save(COMFY)
    print(OUT,COMFY)
    print("person masks",[(n,round(x/W,3)) for n,x,_ in people])

if __name__=="__main__": main()
