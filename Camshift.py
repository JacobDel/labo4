#object that uses camshift and/or viola jones to track face

import cv2 as cv
import numpy as np
import faceGestureRecognitionV2

class FaceTracking:
    face = None
    leftabove = None
    rightunder = None

    def __init__(self,  cap):
        while self.face is None:
            ret, frame = cap.read()
            face = faceGestureRecognitionV2.getFaces(frame)

    def check_viola_jones(self, frame):
        foundFace = faceGestureRecognitionV2.getFaces(frame)
        if foundFace is not None:
            self.face = foundFace

    def PerformFaceTracking(self, frame):
        self.CheckViolaJones(frame)

        # https://docs.opencv.org/3.4/db/df8/tutorial_py_meanshift.html
        
        # setup initial location of window
        track_window = (c, r, w, h)
        # set up the ROI for tracking
        roi = frame[r:r + h, c:c + w]
        hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
