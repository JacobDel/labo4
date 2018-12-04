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
            faces = faceGestureRecognitionV2.getFaces(frame)
            if len(faces) > 0:
                self.face = faces[0]

    def check_viola_jones(self, frame):
        foundFaces = faceGestureRecognitionV2.getFaces(frame)
        if len(foundFaces) != 0:
            self.face = foundFaces[0]

    def PerformFaceTracking(self):
        ret, frame = self.cap.read()
        self.CheckViolaJones(frame)
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

        while(1):
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            # apply meanshift to get the new location
            ret, track_window = cv.CamShift(dst, track_window, term_crit)
            # Draw it on image
            # pts = cv.boxPoints(ret)
            # pts = np.int0(pts)
            # img2 = cv.polylines(frame, [pts], True, 255, 2)
            # cv.imshow('img2', img2)
            # k = cv.waitKey(60) & 0xff
            # if k == 27:
            #     break
            # else:
            #     cv.imwrite(chr(k) + ".jpg", img2)
            self.face = Face(track_window)

