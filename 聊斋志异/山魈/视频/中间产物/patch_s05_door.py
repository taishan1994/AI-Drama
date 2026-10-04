from pathlib import Path
import cv2
import numpy as np

src = Path('/nfs/FM/gongoubo/new_project/github/aigc/AI-Drama/聊斋志异/山魈/视频/source/S05_家人破窗_最终候选.mp4')
dst = Path('/nfs/FM/gongoubo/new_project/github/aigc/AI-Drama/山魈_门缝修复_无音频.avi')
cap = cv2.VideoCapture(str(src))
fps = cap.get(cv2.CAP_PROP_FPS) or 24
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(str(dst), cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
while True:
    ok, frame = cap.read()
    if not ok:
        break
    roi = cv2.cvtColor(frame[70:460, 730:767], cv2.COLOR_BGR2GRAY)
    surrounding = cv2.cvtColor(frame[70:460, 700:730], cv2.COLOR_BGR2GRAY)
    if float(roi.mean()) > float(surrounding.mean()) + 28:
        mask = np.zeros((h, w), np.uint8)
        mask[70:460, 730:767] = 255
        frame = cv2.inpaint(frame, mask, 5, cv2.INPAINT_TELEA)
    out.write(frame)
cap.release(); out.release()
