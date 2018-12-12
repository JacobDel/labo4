import cv2
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
leftEyeInitialised = False
counter = 0
startTime = None
timerResult = None
timerSet = False
face = None
winkEyeX = None
winkEyeY = None
faceSample = None

def scaleEye(eyeImage):
    # NEEDED WHEN THE EYE IMAGE IS TOO LARGE
    # eyeWidth = len(eyeImage[0])
    # eyeHeight = len(eyeImage)
    # return eyeImage[int(eyeWidth/8):int(7*eyeWidth/8),int(eyeHeight/8):int(7*eyeHeight/8)]
    return eyeImage

# setup
faceTracker = FaceTracker(vc)
while leftEyeInitialised is False:
    faceTracker.performFaceTracking()
    leftEye,rightEye=faceTracker.getEyes()
    if (leftEye is not None and rightEye is not None):
        MHIv2.nextFrame(scaleEye(leftEye))
        leftEyeInitialised = True
# loop
while rval:
    faceTracker.performFaceTracking()
    # frameCount = (frameCount+1) % 15 # should only detect faces every x amount of frames, to receive a better framerate
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    wink = False
    leftEye, rightEye = faceTracker.getEyes()
    if (leftEye is not None and rightEye is not None):
        MHIeye = MHIv2.nextFrame(scaleEye(leftEye))
        cv2.imshow("a", MHIeye)
        cv2.imshow("oog",scaleEye(leftEye))
        if WinkRecognition.getWinkRecognition(MHIeye):
            wink = True
    if wink:
        cv2.imshow("effect", frame)
    else:
        cv2.imshow("effect",cv2.resize(frame,(100,80)))
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")