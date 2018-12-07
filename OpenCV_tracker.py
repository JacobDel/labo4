import cv2
import sys

# object that uses camshift and/or viola jones to track face

import cv2 as cv
import faceGestureRecognitionV2
import threading


class FaceTracking:
    face = None
    cap = None

    tracker_head = None
    tracker_eyeL = None
    tracker_eyeR = None

    roi_eyeL = None
    roi_eyeR = None
    roi_head = None

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    def __init__(self, i_cap):
        self.cap = i_cap
        tracker = cv2.Tracker_create('MEDIANFLOW')

        # Define an initial bounding box
        bbox = (287, 23, 86, 320)

        # Uncomment the line below to select a different bounding box
        bbox = cv2.selectROI(frame, False)

        # Initialize tracker with first frame and bounding box
        ok = tracker.init(frame, bbox)

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
                if face.leftEyeX is not None and face.startX is not None:
                    self.face = face
                    self.tracker_head = cv2.TrackerCSRT_create()
                    self.tracker_head = tracker.init(frame, (face.startX, face.startY, face.width, face.height))
                    self.tracker_eyeL = cv2.TrackerCSRT_create()
                    self.tracker_eyeL = tracker.init(frame, (face.leftEyeX, face.leftEyeY, (face.width, face.height)))
                    self.tracker_eyeR = cv2.TrackerCSRT_create()
                    self.tracker_eyeR = tracker.init(frame, (face.rightEyeX, face.rightEyeY, (face.width, face.height)))
                    cv.destroyAllWindows()
            cv.waitKey(1)

    def check_viola_jones(self, frame):
        foundFaces = faceGestureRecognitionV2.getFaces(frame)
        if len(foundFaces) != 0:
            face = foundFaces[0]
            if face.startX is not None:
                self.face.setHead(face.startX, face.startY, face.width, face.height)
                # self.cam_head.roi_setup(frame, face.startX, face.startY, face.width, face.height)

            if face.leftEyeX is not None and face.startX is not None:
                self.face.setEyes(face.leftEyeX, face.leftEyeY, face.rightEyeX, face.rightEyeY, face.eyeWidth,
                                  face.eyeHeight)

                # self.cam_lefteye.roi_setup(frame, face.leftEyeX, face.leftEyeY, face.eyeWidth, face.eyeHeight)


                self.face.setEyes(face.leftEyeX, face.leftEyeY, face.rightEyeX, face.rightEyeY, face.eyeWidth,
                                  face.eyeHeight)

    def Track(self, frame, tracker):

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Draw bounding box
        if ok:
        #     Tracking success


            # p1 = (int(bbox[0]), int(bbox[1]))
            # p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            # cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        # else:
        #     Tracking failure
            # cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
1
        # Display tracker type on frame
        # cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display result
        # cv2.imshow("Tracking", frame)


    def timer(self):
        self.check_timer = True
        threading.Timer(1, self.timer).start()

    def PerformFaceTracking(self):
        ret, frame = self.cap.read()
        if self.check_timer:
            self.check_viola_jones(frame)
            self.check_timer = False
        else:
            # https://docs.opencv.org/3.4/db/df8/tutorial_py_meanshift.html
            ret, track_window = self.MeanShiftTracking(self.cam_head, frame)
            self.face.setHead(track_window[0], track_window[1], track_window[2], track_window[3])
            ret, track_window_left = self.MeanShiftTracking(self.cam_lefteye, frame)
            ret, track_window_right = self.MeanShiftTracking(self.cam_righteye, frame)
            self.face.setEyes(track_window_left[0], track_window_left[1], track_window_right[0], track_window_right[1],track_window_right[2], track_window_right[3])
