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

    frame = None

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
            foundface = foundfaces[0]
            if foundface.startX is not None:
                self.face.setHead(foundface.startX, foundface.startY, foundface.width, foundface.height)
                self.tracker_head = cv2.TrackerCSRT_create()
                self.tracker_head.init(frame, (foundface.startX, foundface.startY, foundface.width, foundface.height))
            if foundface.rightEyeX is not None and foundface.leftEyeX is not None:
                ok = True
                distance_between_eyes = foundface.rightEyeX - foundface.leftEyeX
                if distance_between_eyes < foundface.eyeWidth:
                    ok = False #checks that the distance between the eyes is bigger than the eyewidth
                if foundface.leftEyeX > foundface.rightEyeX:
                    ok = False  #checks that the left eye is to the left of the right eye
                height_difference_between_eyes = abs(foundface.rightEyeY - foundface.leftEyeY)
                if height_difference_between_eyes > distance_between_eyes/2:
                    ok = False
                if ok:
                    if len(self.eyedimension_keeper) > 3:
                        self.eyedimension_keeper.remove(self.eyedimension_keeper[0])
                    self.eyedimension_keeper.append((foundface.eyeWidth, foundface.eyeHeight))
                    width = 0
                    height = 0
                    for i in self.eyedimension_keeper:
                        width = width + i[0]
                        height = height + i[1]
                    width = int(round(width/len(self.eyedimension_keeper)))
                    height = int(round(height/len(self.eyedimension_keeper)))
                    self.face.setEyes(foundface.leftEyeX, foundface.leftEyeY, foundface.rightEyeX, foundface.rightEyeY, width, height)
                    self.tracker_eyeR = cv2.TrackerCSRT_create()
                    self.tracker_eyeR.init(frame, (foundface.rightEyeX, foundface.rightEyeY, width, height))
                    self.tracker_eyeL = cv2.TrackerCSRT_create()
                    self.tracker_eyeL.init(frame, (foundface.leftEyeX, foundface.leftEyeY, width, height))

    def timer(self):
        self.check_timer = True
        threading.Timer(1, self.timer).start()

    def getEyes(self):
        face = self.face
        return self.frame[face.leftEyeY: face.leftEyeY + face.eyeHeight, face.leftEyeX: face.leftEyeX + face.eyeWidth],\
               self.frame[face.rightEyeY: face.rightEyeY + face.eyeHeight, face.rightEyeX: face.rightEyeX + face.eyeWidth]

    def performFaceTracking(self):
        ret, self.frame = self.cap.read()
        if self.check_timer:
            self.check_viola_jones(self.frame)
            self.check_timer = False
        else:
            # https://docs.opencv.org/3.4/db/df8/tutorial_py_meanshift.html
            ok_head, track_window = self.tracker_head.update(self.frame)
            track_window = [int(i) for i in track_window]
            self.face.setHead(track_window[0], track_window[1], track_window[2], track_window[3])
            ok_Leye, track_window_left = self.tracker_eyeL.update(self.frame)
            track_window_left = [int(i) for i in track_window_left]
            ok_Reye, track_window_right = self.tracker_eyeR.update(self.frame)
            track_window_right = [int(i) for i in track_window_right]
            self.face.setEyes(track_window_left[0], track_window_left[1], track_window_right[0], track_window_right[1],
                              self.face.eyeWidth, self.face.eyeHeight)
