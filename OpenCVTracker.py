import cv2
import sys

# object that uses camshift and/or viola jones to track face

import cv2 as cv
import faceGestureRecognitionV2
import threading
import numpy as np


class FaceTracker:
    face = None
    cap = None

    tracker_head = None
    tracker_eyeL = None
    tracker_eyeR = None

    check_timer = False

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

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
                                 (face.leftEyeX+face.eyeWidth,face.leftEyeY+face.eyeHeight),
                                 (255,0,0),2)
                cv.imshow('looking for face', frame)
                if face.leftEyeX is not None and face.startX is not None and face.rightEyeX is not None:
                    self.face = face
                    self.tracker_head = cv2.TrackerCSRT_create()
                    self.tracker_head.init(frame, (face.startX, face.startY, face.width, face.height))
                    self.tracker_eyeL = cv2.TrackerCSRT_create()
                    self.tracker_eyeL.init(frame, (face.leftEyeX, face.leftEyeY, face.eyeWidth, face.eyeHeight))
                    self.tracker_eyeR = cv2.TrackerCSRT_create()
                    self.tracker_eyeR.init(frame, (face.rightEyeX, face.rightEyeY, face.eyeWidth, face.eyeHeight))
                    cv.destroyAllWindows()

                    self.timer()
            cv.waitKey(1)

    def check_viola_jones(self, frame):
        foundfaces = faceGestureRecognitionV2.getFaces(frame)
        if len(foundfaces) != 0:
            face = foundfaces[0]
            if face.startX is not None:
                self.face.setHead(face.startX, face.startY, face.width, face.height)
                self.tracker_head = cv2.TrackerCSRT_create()
                self.tracker_head.init(frame, (face.startX, face.startY, face.width, face.height))
            if face.rightEyeX is not None:
                self.face.setEyes(face.leftEyeX, face.leftEyeY, self.face.rightEyeX, self.face.rightEyeY, face.eyeWidth,
                                  face.eyeHeight)
                self.tracker_eyeR = cv2.TrackerCSRT_create()
                self.tracker_eyeR.init(frame, (face.rightEyeX, face.rightEyeY, face.eyeWidth, face.eyeHeight))
            if face.leftEyeX is not None:
                self.face.setEyes(self.face.leftEyeX, self.face.leftEyeY, face.rightEyeX, face.rightEyeY, face.eyeWidth,
                                  face.eyeHeight)
                self.tracker_eyeL = cv2.TrackerCSRT_create()
                self.tracker_eyeL.init(frame, (face.leftEyeX, face.leftEyeY, face.eyeWidth, face.eyeHeight))

    def timer(self):
        self.check_timer = True
        threading.Timer(2, self.timer).start()

    def PerformFaceTracking(self):
        ret, frame = self.cap.read()
        if self.check_timer:
            self.check_viola_jones(frame)
            self.check_timer = False
        else:
            # https://docs.opencv.org/3.4/db/df8/tutorial_py_meanshift.html
            ok_head, track_window = self.tracker_head.update(frame)
            track_window = [int(i) for i in track_window]
            self.face.setHead(track_window[0], track_window[1], track_window[2], track_window[3])
            ok_Leye, track_window_left = self.tracker_eyeL.update(frame)
            track_window_left = [int(i) for i in track_window_left]
            ok_Reye, track_window_right = self.tracker_eyeR.update(frame)
            track_window_right = [int(i) for i in track_window_right]
            self.face.setEyes(track_window_left[0], track_window_left[1], track_window_right[0], track_window_right[1],
                              self.face.eyeWidth, self.face.eyeHeight)
