from pathlib import Path
import cv2
import numpy as np

src = Path('/nfs/FM/gongoubo/new_project/github/aigc/聊斋志异/山魈/视频/source/S01_门闩里的爪_v2_待验收.mp4')
dst = Path('/nfs/FM/gongoubo/new_project/github/aigc/山魈_S01_去红_无音频.avi')
cap = cv2.VideoCapture(str(src))
fps = cap.get(cv2.CAP_PROP_FPS) or 24
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(str(dst), cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
while True:
    ok, frame = cap.read()
    if not ok:
        break
    roi = frame[120:600, 500:1020]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    red = ((hsv[..., 0] < 16) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 55) & (hsv[..., 2] > 30)
    hsv[..., 1][red] = (hsv[..., 1][red] * 0.18).astype(np.uint8)
    hsv[..., 2][red] = (hsv[..., 2][red] * 0.78).astype(np.uint8)
    frame[120:600, 500:1020] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    out.write(frame)
cap.release(); out.release()
