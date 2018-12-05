import cv2 as cv
import numpy as np


class CamShiftObject:
    hsv_roi = None
    roi = None
    track_window = None
    roi_hist = None
    mask = None
    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

    def __init__(self, frame, x, y, w, h):
        self.roi_setup(frame, x, y, w, h)

    def roi_setup(self, frame, x, y, w, h):
        self.track_window = (x, y, w, h)
        self.roi = frame[y:y+h, x:x+w]
        self.hsv_roi = cv.cvtColor(self.roi, cv.COLOR_BGR2HSV)
        self.mask = cv.inRange(self.hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        self.roi_hist = cv.calcHist([self.hsv_roi], [0], self.mask, [180], [0, 180])
        cv.normalize(self.roi_hist, self.roi_hist, 0, 255, cv.NORM_MINMAX)