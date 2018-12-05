#object that uses camshift and/or viola jones to track face

import cv2 as cv
import faceGestureRecognitionV2
from CamShiftObject import CamShiftObject


class FaceTracking:
    face = None
    leftabove = None
    rightunder = None
    cap = None

    # these are needed to find the angle under which the box is rotated
    headangle = None
    lefteyeangle = None
    righteyeangle = None

    # these are used to indicate f camshift is required, if the eye has been detected by viola_jones, then camshift is
    # unnecessary
    foundhead = False
    foundlefteye = False
    foundrighteye = False

    cam_head = None
    cam_lefteye = None
    cam_righteye = None

#for showing the squares
    rethead = None
    retlefteye = None
    retrighteye = None

    def __init__(self, i_cap):
        self.cap = i_cap
        while self.face is None:
            ret, frame = i_cap.read()
            faces = faceGestureRecognitionV2.getFaces(frame)
            cv.imshow('looking for face', frame)
            if len(faces) > 0:
                face = faces[0]
                cv.rectangle(frame, (face.startX, face.startY), (face.startX + face.width, face.startY + face.height),
                             (255, 0, 0), 2)
                if face.leftEyeY:
                    cv.rectangle(frame,(face.leftEyeX,face.leftEyeY),
                                 (face.leftEyeX+face.leftEyeWidth,face.leftEyeY+face.leftEyeHeight),
                                 (255,0,0),2)
                # if face.rightEyeX:
                    # cv.rectangle(frame, (face.rightEyeX, face.rightEyeY),
                    #              (face.rightEyeX + face.rightEyeWidth, face.rightEyeY + face.rightEyeHeight),
                    #              (255, 0, 0), 2)
                cv.imshow('looking for face', frame)
                if face.leftEyeX is not None and face.rightEyeX is not None and face.startX is not None:
                    self.face = face
                    self.headangle = 0
                    self.rethead = ((face.startX + face.width/2, face.startY + face.height/2), (face.width, face.height), 0)
                    self.cam_head = CamShiftObject(frame, face.startX, face.startY, face.width, face.height)

                    self.lefteyeangle = 0
                    self.retlefteye = ((face.leftEyeX + face.leftEyeWidth/2, face.leftEyeY + face.leftEyeHeight/2),(face.leftEyeWidth, face.leftEyeHeight), 0)
                    self.cam_lefteye = CamShiftObject(frame, face.leftEyeX, face.leftEyeY, face.leftEyeWidth, face.leftEyeHeight)

                    self.righteyeangle = 0
                    # self.retrighteye = ((face.rightEyeX + face.rightEyeWidth/2, face.rightEyeY + face.rightEyeHeight/2),(face.rightEyeWidth, face.rightEyeHeight), 0)
                    # self.cam_righteye = CamShiftObject(frame, face.rightEyeX, face.rightEyeY, face.rightEyeWidth, face.rightEyeHeight)
                    self.lastframe = frame
                    cv.destroyAllWindows()
            cv.waitKey(1)

    def check_viola_jones(self, frame):
        foundFaces = faceGestureRecognitionV2.getFaces(frame)
        self.foundlefteye = False
        self.foundrighteye = False
        self.foundhead = False
        if len(foundFaces) != 0:
            face = foundFaces[0]
            if face.leftEyeX is not None:
                self.face.setLeftEye(face.leftEyeX, face.leftEyeY, face.leftEyeWidth, face.leftEyeHeight)
                self.foundlefteye = True
                self.retlefteye = ((face.leftEyeX + face.leftEyeWidth / 2, face.leftEyeY + face.leftEyeHeight / 2),
                                   (face.leftEyeWidth, face.leftEyeHeight), 0)
                self.cam_lefteye.roi_setup(frame, face.leftEyeX, face.leftEyeY, face.leftEyeWidth, face.leftEyeHeight)

            if face.rightEyeX is not None:
                self.face.setRightEye(face.rightEyeX, face.rightEyeY, face.rightEyeWidth, face.rightEyeHeight)
                self.foundrighteye = True
                # self.retrighteye = ((face.rightEyeX + face.rightEyeWidth / 2, face.rightEyeY + face.rightEyeHeight / 2),
                #                     (face.rightEyeWidth, face.rightEyeHeight), 0)
                # self.cam_righteye.roi_setup(frame, face.rightEyeX, face.rightEyeY, face.rightEyeWidth, face.rightEyeHeight)

            if face.startX is not None:
                self.foundhead = True
                self.face.setHead(face.startX, face.startY, face.width, face.height)
                self.rethead = ((face.startX + face.width/2, face.startY + face.height/2), (face.width, face.height), 0)
                self.cam_head.roi_setup(frame, face.startX, face.startY, face.width, face.height)

    # def CamshiftTracking(self, frame, x, y, w, h):
        # # setup initial location of window
        # track_window = (y, x, w, h)
        # # set up the ROI for tracking
        # roi = frame[y:y + h, x:x + w]
        # hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        # mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        # roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        # cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        # # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        # term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        #
        # hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        # # apply meanshift to get the new location
        # ret, track_window = cv.CamShift(dst, track_window, term_crit)
        # # return track_window
        # # self.face = Face(track_window[0], track_window[1], track_window[2], track_window[3])
        # # self.ret = ret
        # return ret, track_window

    # TODO: de fout is:  er wordt een stuk uitgeknipt uit een foto en dan wordt dit stuk getracked op dezelfde foto
    def CamshiftTracking(self, cam_tracker, frame):
        track_window = cam_tracker.track_window
        # set up the ROI for tracking
        roi_hist = cam_tracker.roi_hist
        term_crit = cam_tracker.term_crit


        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        # apply meanshift to get the new location
        ret, track_window = cv.CamShift(dst, track_window, term_crit)

        return ret, track_window

    def PerformFaceTracking(self):
        ret, frame = self.cap.read()
        # self.check_viola_jones(frame)
        # https://docs.opencv.org/3.4/db/df8/tutorial_py_meanshift.html
        self.foundhead = False
        if not self.foundhead:
            ret, track_window = self.CamshiftTracking(self.cam_head, frame)
            # ret, track_window = self.CamshiftTracking(frame,
            #                                           self.face.startX,
            #                                           self.face.startY,
            #                                           self.face.width,
            #                                           self.face.height)
            self.headangle = ret[2]
            self.rethead = ret
            self.face.setHead(track_window[0], track_window[1], track_window[2], track_window[3])
        if not self.foundlefteye:
            ret, track_window = self.CamshiftTracking(self.cam_lefteye, frame)
            # ret, track_window = self.CamshiftTracking(frame,
            #                                           self.face.leftEyeX,
            #                                           self.face.leftEyeY,
            #                                           self.face.leftEyeWidth,
            #                                           self.face.leftEyeHeight)
            self.lefteyeangle = ret[2]
            self.retlefteye = ret
            self.face.setLeftEye(track_window[0], track_window[1], track_window[2], track_window[3])

        # if not self.foundrighteye:
            # ret, track_window = self.CamshiftTracking(self.cam_righteye, frame)
            # ret, track_window = self.CamshiftTracking(frame,
            #                                           self.face.rightEyeX,
            #                                           self.face.rightEyeY,
            #                                           self.face.rightEyeWidth,
            #                                           self.face.rightEyeHeight)
            # self.righteyeangle = ret[2]
            # self.face.setRightEye(track_window[0], track_window[1], track_window[2], track_window[3])
        self.lastframe = frame