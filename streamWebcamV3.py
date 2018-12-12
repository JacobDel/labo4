import cv2
from faceGestureRecognitionV2 import getFaces
import time
import sys
# from Tracker import FaceTracking
import Tracker
import WinkRecognition
import MHIv2
from OpenCVTracker import FaceTracker


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

def scaleEye(eyeImage):
    # eyeWidth = len(eyeImage[0])
    # eyeHeight = len(eyeImage)
    # return eyeImage[int(eyeWidth/8):int(7*eyeWidth/8),int(eyeHeight/8):int(7*eyeHeight/8)]
    return eyeImage

# setup
faceTracker = FaceTracker(vc)
while leftEyeInitialised is False:
    faceTracker.performFaceTracking()
    leftEye,rightEye=faceTracker.getEyes()
    if (leftEye is not None and rightEye is not None):  # unsupported operand type(s) for &: 'NoneType' and 'NoneType'
        # eyes are found
        # prevLeftEye = frame[face.leftEyeY:face.leftEyeY + face.eyeHeight,
        #               face.leftEyeX:face.leftEyeX + face.eyeWidth]
        # faceSample = frame[face.leftEyeY:face.leftEyeY + face.eyeHeight,
        #               face.leftEyeX+face.eyeWidth:face.leftEyeX + 2*face.eyeWidth]
        # prevLeftEye = eyes[0]
        # prevLeftEye = leftEye
        MHIv2.nextFrame(scaleEye(leftEye))
        leftEyeInitialised = True



# loop
while rval:
    faceTracker.performFaceTracking()
    # frameCount = (frameCount+1) % 15 # should only detect faces every x amount of frames
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    # if frameCount == 1:
    # faces = getFaces(frame)


    # if len(faces) is 1:
    #     face = faces[0]
    #     cv2.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,150,0),2)
    #     if face.leftEyeX:
    #         cv2.rectangle(frame, (face.leftEyeX, face.leftEyeY), (face.leftEyeX + face.eyeWidth, face.leftEyeY + face.eyeHeight),
    #                       (255, 0, 123), 2)
    #     if face.rightEyeX:
    #         cv2.rectangle(frame, (face.rightEyeX, face.rightEyeY), (face.rightEyeX + face.eyeWidth, face.rightEyeY + face.eyeHeight),
    #                       (0, 100, 123), 2)


        # prevRightEye = frame[face.rightEyeY:face.rightEyeY + face.height, face.rightEyeX:face.rightEyeX + face.eyeWidth]
    # if leftEyeInitialised:
        # also give the head to check if the head moved!
    wink = False
    leftEye, rightEye = faceTracker.getEyes()
    if (leftEye is not None and rightEye is not None):
        MHIeye = MHIv2.nextFrame(scaleEye(leftEye))
        # MHImoved = MHIv2.nextFrame(faceSample)
        cv2.imshow("a", MHIeye)
        cv2.imshow("oog",scaleEye(leftEye))

        # if not WinkRecognition.getWinkRecognition(MHImoved):
        if WinkRecognition.getWinkRecognition(MHIeye):
            wink = True

    if wink:
        cv2.imshow("effect", frame)
    else:
        cv2.imshow("effect",cv2.resize(frame,(100,80)))
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