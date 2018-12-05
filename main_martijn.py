import cv2
import cv2 as cv
import numpy as np
from Tracker import FaceTracking

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

frameCount = 0
faces = None
facetracker = FaceTracking(vc)
while rval:
    # frameCount = (frameCount+1) % 15 # should only detect faces every x amount of frames

    cv2.imshow('preview', frame)
    ret, frame = vc.read()
    facetracker.PerformFaceTracking()
    # print(str(facetracker.face.startX) + ", " + str(facetracker.face.startY) + ", " + str(facetracker.face.width) + ", " + str(facetracker.face.height))
    cv2.rectangle(frame,(facetracker.face.startX,facetracker.face.startY),(facetracker.face.startX+facetracker.face.width,facetracker.face.startY+facetracker.face.height),(255,0,0),2)
    pts = cv2.boxPoints(facetracker.ret)
    pts = np.int0(pts)
    img2 = cv.polylines(frame, [pts], True, 255, 2)

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")