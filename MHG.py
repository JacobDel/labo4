import cv2

def GetMHG(mhi):
    min_delta = 0.05
    max_delta = 0.5

    # mg_mask, mg_orient = cv2.calcMotionGradient(mhi, MAX_TIME_DELTA, MIN_TIME_DELTA, apertureSize=5)
    mhi = mhi.astype(dtype="int16")
    mg_mask, mg_orient = cv2.motempl.calcMotionGradient(mhi, min_delta, max_delta, apertureSize=5)
    return mg_mask, mg_orient
