import cv2
import numpy as np

#motion history images

MHI_DURATION = 10
DEFAULT_THRESHOLD = 32


h = None
w = None
prev_frame = []
motion_history = None
timestamp = 0
isInitialized = False

def reset(frame):
    global prev_frame
    global timestamp
    global motion_history
    global h
    global w
    global isInitialized
    h, w = frame.shape[:2]
    prev_frame = frame.copy()
    motion_history = np.zeros((h, w), np.float32)
    timestamp = 0
    isInitialized = True

def nextFrame(frame):
    global prev_frame
    global timestamp
    global motion_history
    global h
    global w
    if not isInitialized:
        reset(frame)
        return frame
    else:
        frame=cv2.resize(frame,(w,h))
        frame_diff = cv2.absdiff(frame, prev_frame)
        gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        ret, fgmask = cv2.threshold(gray_diff,DEFAULT_THRESHOLD,1,cv2.THRESH_BINARY)
        timestamp += 1

        # update motion history
        cv2.motempl.updateMotionHistory(fgmask, motion_history, timestamp, MHI_DURATION)

        # normalize motion history
        mh = np.uint8(np.clip((motion_history-(timestamp-MHI_DURATION))/MHI_DURATION,0,1)*255)

        prev_frame = frame.copy()
        return mh