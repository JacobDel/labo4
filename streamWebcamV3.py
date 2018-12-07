import cv2
from faceGestureRecognitionV2 import getFaces
import time
import sys
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
# if head is found but the eyes aren't! for +-2sec
counter = 0
startTime = None
timerResult = None
timerSet = False
face = None
winkEyeX = None
winkEyeY = None
faceSample = None

# setup




# loop
while rval:

    # frameCount = (frameCount+1) % 15 # should only detect faces every x amount of frames
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    # if frameCount == 1:
    faces = getFaces(frame)
    if len(faces) is 1:
        face = faces[0]
        cv2.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,150,0),2)
        if face.leftEyeX:
            cv2.rectangle(frame, (face.leftEyeX, face.leftEyeY), (face.leftEyeX + face.eyeWidth, face.leftEyeY + face.eyeHeight),
                          (255, 0, 123), 2)
        if face.rightEyeX:
            cv2.rectangle(frame, (face.rightEyeX, face.rightEyeY), (face.rightEyeX + face.eyeWidth, face.rightEyeY + face.eyeHeight),
                          (0, 100, 123), 2)

        if (faces[0].leftEyeY):  # unsupported operand type(s) for &: 'NoneType' and 'NoneType'
            # eyes are found
            prevLeftEye = frame[face.leftEyeY:face.leftEyeY + face.eyeHeight,
                          face.leftEyeX:face.leftEyeX + face.eyeWidth]
            faceSample = frame[face.leftEyeY:face.leftEyeY + face.eyeHeight,
                          face.leftEyeX+face.eyeWidth:face.leftEyeX + 2*face.eyeWidth]
            leftEyeInitialised = True
            # prevRightEye = frame[face.rightEyeY:face.rightEyeY + face.height, face.rightEyeX:face.rightEyeX + face.eyeWidth]
        if leftEyeInitialised:
            # also give the head to check if the head moved!
            MHIeye = MHIv2.nextFrame(prevLeftEye)
            MHImoved = MHIv2.nextFrame(faceSample)
            cv2.imshow("a", MHIeye)

            if not WinkRecognition.getWinkRecognition(MHImoved):
                if WinkRecognition.getWinkRecognition(MHIeye):
                    print("knipoog")

        print("-----")
        # # check if eyes exist
        # if face.leftEyeX is None:
        #     # search the eyes closest to our previous eye
        #     # start timer



        #     if timerSet is False:
        #         startTime = time.time()
        #         timerSet = True
        #         print("timer set")
        # else:
        #     # stop timer
        #     if timerSet:
        #         timerResult = time.time()-startTime
        #         print(timerResult)
        #         print("timer stopped")
    # else:
    #     face = None
    #
    # if face is not None:
    #
    # else:
    #     timerSet=False




    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")