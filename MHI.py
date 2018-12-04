import cv2
import numpy as np

MHI_DURATION = 10
DEFAULT_THRESHOLD = 32

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
h, w =frame.shape[:2]
prev_frame = frame.copy()
motion_history = np.zeros((h,w),np.float32)
timestamp = 0
while True:
    ret, frame = cam.read()
    if not ret:
        break
    frame_diff = cv2.absdiff(frame, prev_frame)
    gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    ret, fgmask = cv2.threshold(gray_diff,DEFAULT_THRESHOLD,1,cv2.THRESH_BINARY)
    timestamp += 1

    # update motion history
    cv2.motempl.updateMotionHistory(fgmask, motion_history, timestamp, MHI_DURATION)

    # normalize motion history
    mh = np.uint8(np.clip((motion_history-(timestamp-MHI_DURATION))/MHI_DURATION,0,1)*255)
    cv2.imshow('motempl', mh)
    cv2.imshow('raw', frame)

    prev_frame = frame.copy()
    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()