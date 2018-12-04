#object that uses camshift and/or viola jones to track face

import cv2 as cv
import numpy as np
import faceGestureRecognitionV2
from faceObject import Face

class FaceTracking:
    face = None
    leftabove = None
    rightunder = None
    cap = None

    def __init__(self, i_cap):
        self.cap = i_cap
        while self.face is None:
            ret, frame = i_cap.read()
            cv.imshow('looking for face', frame)
            cv.waitKey(1)
            faces = faceGestureRecognitionV2.getFaces(frame)
            if len(faces) > 0:
                self.face = faces[0]
                cv.destroyAllWindows()

    def check_viola_jones(self, frame):
        foundFaces = faceGestureRecognitionV2.getFaces(frame)
        if len(foundFaces) != 0:
            self.face = foundFaces[0]

    def PerformFaceTracking(self):
        ret, frame = self.cap.read()
        self.check_viola_jones(frame)
        # https://docs.opencv.org/3.4/db/df8/tutorial_py_meanshift.html

        # setup initial location of window
        self.face.startX
        x, y, w, h = self.face.startX, self.face.startY, self.face.width, self.face.height
        track_window = (x, y, w, h)
        # set up the ROI for tracking
        roi = frame[y:y + h, x:x + w]
        hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            # apply meanshift to get the new location
        ret, track_window = cv.CamShift(dst, track_window, term_crit)
        self.face = Face(track_window[0], track_window[1], track_window[3], track_window[2])

