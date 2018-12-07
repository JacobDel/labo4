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
prevLeftEye = None
prevRightEye = None
leftEyeInitialised = False # The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
while rval:
    frameCount = (frameCount+1) % 15 # should only detect faces every x amount of frames
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    if frameCount == 1:
        faces = getFaces(frame)
    for face in faces:
        cv2.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,0,0),2)
    # in faces get face[0]
    # cut out the eye image
    if len(faces)>0:
        if(faces[0].leftEyeY and faces[0].rightEyeY): # unsupported operand type(s) for &: 'NoneType' and 'NoneType'
            # eyes are found
            prevLeftEye = frame[face.leftEyeY:face.leftEyeY+face.eyeHeight, face.leftEyeX:face.leftEyeX+face.eyeWidth]
            leftEyeInitialised=True
            # prevRightEye = frame[face.rightEyeY:face.rightEyeY + face.height, face.rightEyeX:face.rightEyeX + face.eyeWidth]
        if leftEyeInitialised:
            # also give the head to check if the head moved!
            MHIeye = MHIv2.nextFrame(prevLeftEye)
            cv2.imshow("test",MHIeye)
            if WinkRecognition.getWinkRecognition(MHIeye):
                print("knipoog")


    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")