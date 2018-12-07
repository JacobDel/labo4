import cv2
import cv2 as cv
import numpy as np
from HeadTiltDetectorv2 import TiltDetector
from HeadNodDetection import nodDetector
from Tracker import FaceTracking
from ImageController import image_controller
import MHIv3 as MHI

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

frameCount = 0
faces = None
facetracker = FaceTracking(vc)
cv2.destroyWindow("preview")
tiltdetector = TiltDetector()
noddetector = nodDetector()
MHI.reset(vc.read()[1])
cv.waitKey(2)
MHI.nextFrame(vc.read()[1])

# any image can be passed along to be displayed
image_controller = image_controller(vc.read()[1])

"""
does stuff like tracking face, tracking eyes and such
"""
def perform_tests():
    ret, frame = vc.read()
    mhi = MHI.nextFrame(frame)
    facetracker.PerformFaceTracking()
    # print(str(facetracker.face.startX) + ", " + str(facetracker.face.startY) + ", " + str(facetracker.face.width) + ", " + str(facetracker.face.height))
    # cv2.rectangle(frame,(facetracker.face.startX,facetracker.face.startY),(facetracker.face.startX+facetracker.face.width,facetracker.face.startY+facetracker.face.height),(255,0,0),2)

    # pts = cv2.boxPoints(facetracker.rethead)
    # pts = np.int0(pts)
    # frame = cv.polylines(frame, [pts], True, 255, 2)
    # pts = cv2.boxPoints(facetracker.retlefteye)
    # pts = np.int0(pts)
    # frame = cv.polylines(frame, [pts], True, 255, 2)
    # pts = cv2.boxPoints(facetracker.retrighteye)
    # pts = np.int0(pts)
    # frame = cv.polylines(frame, [pts], True, 255, 2)
    face = facetracker.face
    frame = cv2.rectangle(frame, (face.startX, face.startY), (face.startX + face.width, face.startY + face.height), (255,0,0),2)
    # frame = cv2.rectangle(frame, (face.leftEyeX, face.leftEyeY), (face.eyeWidth + face.leftEyeX, face.eyeHeight + face.leftEyeY), (255,0,0),2)
    # frame = cv2.rectangle(frame, (face.rightEyeX, face.rightEyeY), (face.eyeWidth + face.rightEyeX, face.eyeHeight + face.rightEyeY), (255,0,0),2)

    cv2.imshow('preview', frame)


"""
makes checks on the measured data
"""
def perform_checks():
    active = False
    #   headtilt checks
    # if tiltdetector.RightTilt():
    #     image_controller.rotate(1)
    #     active = True
    # elif tiltdetector.LeftTilt():
    #     image_controller.rotate(-1)
    #     active = True

    # headnod checks
    # horizontal, vertical = noddetector.checknods()
    # if horizontal:
    #     image_controller.resize_horizontal()
    #     active = True
    # elif vertical:
    #     image_controller.resize_vertical()
    #     active = True

    if not active:
        image_controller.reset()
    image_controller.show()
    # horizontal, vertical = noddetector.get_values()
    # print(horizontal + "   " + vertical)
    # print(str(tiltdetector.Getaverage()))
"""
the big while loop that runs continuesly
"""
while True:
    perform_tests()
    # code for checking head tilt(leftor right)
    tiltdetector.update(facetracker.headangle)
    #
    # code for checking head nod(vertical or horizontal)
    noddetector.update(facetracker.face)
    perform_checks()

    image_controller.show()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
