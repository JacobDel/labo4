import cv2
from faceGestureRecognitionV2 import getFaces
from Tracker import FaceTracking
import Tracker
import WinkRecognition
import MHIv2


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

frameCount = 0
faces = None
while rval:
    frameCount = (frameCount+1) % 15 # should only detect faces every x amount of frames
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    if frameCount == 1:
        faces = getFaces(frame)
    for face in faces:
        cv2.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,0,0),2)
    img1,img2=Tracker.GetEyes()
    if img1:
        MHIeye = MHIv2.nextFrame(img1)
        cv2.imshow("test",MHIeye)
        if WinkRecognition.getWinkRecognition(MHIeye):
            print("knipoog")


    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")