import cv2
import cv2 as cv
import numpy as np
from HeadTiltDetector import TiltDetector
from Tracker import FaceTracking
from ImageController import image_controller

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
# any image can be passed along to be displayed
image_controller = image_controller(vc.read()[1])

"""
does stuff like tracking face, tracking eyes and such
"""
def perform_tests():
    ret, frame = vc.read()
    facetracker.PerformFaceTracking()
    # print(str(facetracker.face.startX) + ", " + str(facetracker.face.startY) + ", " + str(facetracker.face.width) + ", " + str(facetracker.face.height))
    # cv2.rectangle(frame,(facetracker.face.startX,facetracker.face.startY),(facetracker.face.startX+facetracker.face.width,facetracker.face.startY+facetracker.face.height),(255,0,0),2)
    pts = cv2.boxPoints(facetracker.rethead)
    pts = np.int0(pts)
    frame = cv.polylines(frame, [pts], True, 255, 2)

    pts = cv2.boxPoints(facetracker.retlefteye)
    pts = np.int0(pts)
    frame = cv.polylines(frame, [pts], True, 255, 2)
    cv2.imshow('preview', frame)


"""
makes checks on the measured data
"""
def perform_checks():
    # 
    if tiltdetector.RightTilt():
        image_controller.rotate(1)
    elif tiltdetector.LeftTilt():
        image_controller.rotate(-1)
    else:
        image_controller.reset()


"""
the big while loop that runs continuesly
"""
while True:
    perform_tests()
    # code for checking head tilt(leftor right)
    average = tiltdetector.update(facetracker.headangle)
    #
    # 
    perform_checks()

    image_controller.show()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
