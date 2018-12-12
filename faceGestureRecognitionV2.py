import cv2 as cv
from faceObject import Face

#based on viola jones

#pre load xml files:
face_cascade = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascades/haarcascade_eye.xml')
smile_cascade = cv.CascadeClassifier('haarcascades/haarcascade_eye.xml')

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
    person = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        smiles = smile_cascade.detectMultiScale(roi_gray)

        person.append(Face(int(x*xRatio), int(y*yRatio), int(h*yRatio), int(w*xRatio)))

        if len(eyes) > 0:
            person[0].leftEyeX = int((eyes[0][0]+x)*xRatio)
            person[0].leftEyeY = int((eyes[0][1]+y)*yRatio)
            person[0].eyeWidth = int(eyes[0][2]*xRatio)
            person[0].eyeHeight = int(eyes[0][3]*yRatio)
        if len(eyes) > 1:
            person[0].rightEyeX = int((eyes[1][0]+x)*xRatio)
            person[0].rightEyeY = int((eyes[1][1]+y)*yRatio)
            # set left eye left & right eye right
            if(person[0].rightEyeX<person[0].leftEyeX):
                swapEyeX=person[0].leftEyeX
                swapEyeY=person[0].leftEyeY
                person[0].leftEyeX = person[0].rightEyeX
                person[0].leftEyeY = person[0].rightEyeY
                person[0].rightEyeX = swapEyeX
                person[0].rightEyeY = swapEyeY

        if len(smiles)>0:
            person[0].smileX = int((smiles[0][0]+x)*xRatio)
            person[0].smileY = int((smiles[0][1]+y)*yRatio)
            person[0].smileWidth = int(smiles[0][2]*xRatio)
            person[0].smileHeight = int(smiles[0][3]*yRatio)
    return person

#TO TEST:

# cap = cv.VideoCapture(0)
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     faces = getFaces(frame)
#     for face in faces:
#         cv.rectangle(frame,(face.startX,face.startY),(face.startX+face.width,face.startY+face.height),(255,0,0),2)
#         if face.leftEyeY is not None and face.rightEyeX is not None:
#             cv.rectangle(frame,(face.leftEyeX,face.leftEyeY),(face.leftEyeX+face.eyeWidth,face.leftEyeY+face.eyeHeight),(255,0,0),2)
#             cv.rectangle(frame, (face.rightEyeX, face.rightEyeY),
#                          (face.rightEyeX + face.eyeWidth, face.rightEyeY + face.eyeHeight), (255, 0, 0), 2)
#         if face.smileY:
#             cv.rectangle(frame, (face.smileX, face.smileY),
#                          (face.smileX + face.smileWidth, face.smileY + face.smileHeight), (255, 0, 0), 2)
#     cv.imshow('img', frame)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()