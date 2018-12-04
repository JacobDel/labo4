import numpy as np
import cv2 as cv
import sys
from faceObject import Face

#based on viola jones

#pre load xml files:
face_cascade = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascades/haarcascade_eye.xml')

# https://docs.opencv.org/3.4.3/d7/d8b/tutorial_py_face_detection.htmlq
def getFaces(frame):
    # return array with faces

    #read the frame size before resizing:
    orgWidth = len(frame[0])
    orgHeight = len(frame)

    # resize frame
    frame = cv.resize(frame, (640, 360))

    #factors:
    xRatio = orgWidth/640
    yRatio = orgHeight/360

    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv.imshow('frame', gray)

    # Haar-cascade Detection in OpenCV

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faceWithEyes = []
    for (x, y, w, h) in faces:
        # cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if eyes is not None:
            faceWithEyes.append(Face(int(x*xRatio), int(y*yRatio), int(h*yRatio), int(w*xRatio)))

        # for (ex, ey, ew, eh) in eyes:
            # cv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    return faceWithEyes

#TO TEST:

# cap = cv.VideoCapture(sys.argv[1])
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     faces = getFaces(frame)
#     for face in faces:
#         cv.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,0,0),2)
#
#     cv.imshow('img', frame)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()