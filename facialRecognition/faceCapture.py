import cv2
import numpy as np
import dlib

import utils.libs.logger as logger

detectorFace = dlib.get_frontal_face_detector()
cam = cv2.VideoCapture(0)
id = input('Enter the id here')
sampleNumber = 0

while True :
    ret, img = cam.read()

    faces = detectorFace(img, 1)

    for face in faces :
        sampleNumber = sampleNumber+1
        e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
        cv2.imwrite("dataset/" + str(id) + "." + str(sampleNumber) + ".jpg", img)
        cv2.rectangle(img, (e, t), (d, b), (0, 255, 255), 2)
        cv2.waitKey(100)
    cv2.imshow("Face", img)
    logger.log('Imagem ' + str(sampleNumber) + ' gravada')
    if sampleNumber > 10 :
        break
cam.release()
cv2.destroyAllWindows()
