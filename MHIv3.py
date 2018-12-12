import cv2
import numpy as np

#motion history images

MHI_DURATION = 10
DEFAULT_THRESHOLD = 32


h = None
w = None
prev_frame = None
motion_history = None
timestamp = 0

reset = False

def reset(frame):
    global prev_frame
    global timestamp
    global motion_history
    global h
    global w
    h, w = frame.shape[:2]
    prev_frame = frame.copy()
    motion_history = np.zeros((h, w), np.float32)
    timestamp = 0


def nextFrame(frame):
    if not reset:
        reset(frame)
        return frame
    else:
        global prev_frame
        global timestamp
        global motion_history
        global h
        global w
        frame_diff = cv2.absdiff(frame, prev_frame)
        gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        ret, fgmask = cv2.threshold(gray_diff,DEFAULT_THRESHOLD,1,cv2.THRESH_BINARY)
        timestamp += 1

        # update motion history
        cv2.motempl.updateMotionHistory(fgmask, motion_history, timestamp, MHI_DURATION)

        # mg_mask, mg_orient = cv2.motempl.calcMotionGradient(motion_history, 4, 2, 5)

        # print(str(cv2.motempl.calcGlobalOrientation(mg_orient, mg_mask, motion_history, timestamp, MHI_DURATION)))

        # if (np.sum(mg_mask) > 2000):  # kleine detecties willen we niet
        #     angle = cv2.motempl.calcGlobalOrientation(mg_orient, mg_mask, motion_history, timestamp, MHI_DURATION)
        #     print("bewogen " + str(angle))
            # if (angle < 280 and angle > 265):
            #     print("boven")  # werkt goed
            # elif (angle < 190 and angle > 160):
            #     print("rechts")  # werkt goed
            # elif (angle < 100 and angle > 80):
            #     print("beneden")  # werkt maar soms
            # elif (angle > 320 or angle < 10):
            #     print("links")  # werkt goed

        # normalize motion history
        mh = np.uint8(np.clip((motion_history-(timestamp-MHI_DURATION))/MHI_DURATION,0,1)*255)
        # cv2.imshow('motempl', mh)
        # cv2.imshow('raw', frame)

        prev_frame = frame.copy()
        return mh
    # if 0xFF & cv2.waitKey(5) == 27:
    #     break
# cv2.destroyAllWindows()