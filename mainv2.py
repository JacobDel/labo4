import cv2
import cv2 as cv
from HeadTiltDetectorv2 import TiltDetector
from HeadNodDetectionv2 import nodDetector
from ImageController import image_controller
import MHIv3 as mhi
from OpenCVTracker import FaceTracker

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

frameCount = 0
faces = None
facetracker = FaceTracker(vc)
cv2.destroyWindow("preview")
tiltdetector = TiltDetector()
noddetector = nodDetector()
mhi.reset(vc.read()[1])
cv.waitKey(2)
mhi.nextFrame(vc.read()[1])

# any image can be passed along to be displayed
image_controller = image_controller(vc.read()[1])

"""
does stuff like tracking face, tracking eyes and such
"""
def perform_tests():
    ret, frame = vc.read()
    mhi_value = mhi.nextFrame(frame)
    facetracker.performFaceTracking()
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
    frame = cv2.rectangle(frame, (face.leftEyeX, face.leftEyeY), (face.eyeWidth + face.leftEyeX, face.eyeHeight + face.leftEyeY), (255,0,0),2)
    frame = cv2.rectangle(frame, (face.rightEyeX, face.rightEyeY), (face.eyeWidth + face.rightEyeX, face.eyeHeight + face.rightEyeY), (255,0,0),2)
    eyeleft, eyeright = facetracker.getEyes()
    # cv2.imshow("lefteye", eyeleft)
    # cv2.imshow("righteye", eyeright)
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
    horizontal, vertical = noddetector.getNods()
    if horizontal:
        image_controller.resize_horizontal()
        active = True
    elif vertical:
        image_controller.resize_vertical()
        active = True

    if horizontal:
        print("horizontal")
    if vertical:
        print("vertical")

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
    # tiltdetector.update(facetracker.headangle)

    # code for checking head nod(vertical or horizontal)
    noddetector.update(facetracker.face)
    perform_checks()

    image_controller.show()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break