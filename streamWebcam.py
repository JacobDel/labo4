import cv2
from faceGestureRecognitionV2 import getFaces
from Camshift import FaceTracking

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

frameCount = 0
faces = None

facetracker = FaceTracking(vc)
while rval:
    frameCount = (frameCount+1) % 30 # should only take detect faces every 30 frames
    cv2.imshow("preview", frame)
    cv2.waitKey(1)
    rval, frame = vc.read()
    if frameCount == 1:
        facetracker.PerformFaceTracking(frame)
        face = facetracker.face
        cv2.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,0,0),2)

        # faces = getFaces(frame)
    # for face in faces:
    #     cv2.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,0,0),2)


    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")