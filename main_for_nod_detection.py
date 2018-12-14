import cv2
import cv2 as cv
from HeadNodDetectionv2 import nodDetector
from ImageController import image_controller
from OpenCVTracker import FaceTracker

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

frameCount = 0
faces = None
facetracker = FaceTracker(vc)
cv2.destroyWindow("preview")
noddetector = nodDetector()
cv.waitKey(2)

# any image can be passed along to be displayed
image_controller = image_controller(vc.read()[1])

"""
does stuff like tracking face, tracking eyes and such
"""
def perform_tests():
    ret, frame = vc.read()
    facetracker.performFaceTracking()

    face = facetracker.face
    frame = cv2.rectangle(frame, (face.startX, face.startY), (face.startX + face.width, face.startY + face.height), (255,0,0),2)
    frame = cv2.rectangle(frame, (face.leftEyeX, face.leftEyeY), (face.eyeWidth + face.leftEyeX, face.eyeHeight + face.leftEyeY), (255,0,0),2)
    frame = cv2.rectangle(frame, (face.rightEyeX, face.rightEyeY), (face.eyeWidth + face.rightEyeX, face.eyeHeight + face.rightEyeY), (255,0,0),2)
    cv2.imshow('preview', frame)


"""
makes checks on the measured data
"""
def perform_checks():
    active = False
    # headtilt does not work with the OpenCV tracker
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

    print(str(noddetector.x_total) + "    " + str(noddetector.y_total))
    # if horizontal:
    #     print("horizontal")
    # if vertical:
    #     print("vertical")

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
