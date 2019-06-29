import cv2
import numpy as np
import dlib
import utils.libs.db as db
import imutils


def captureNewFace(sName, messageHUB) :
    detectorFace = dlib.get_frontal_face_detector()
    cam = cv2.VideoCapture(0)

    iId = db.getNextId()
    sampleNumber = 0



    while True:
        i, img = cam.read()
        faces = detectorFace(img, 1)

        for face in faces:
            if sampleNumber < 10:

                sampleNumber = sampleNumber+1
                e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
                cv2.imwrite("dataset/" + str(iId) + "." + str(sampleNumber) + ".jpg", img)
                cv2.rectangle(img, (e, t), (d, b), (0, 255, 255), 2)
                cv2.waitKey(100)
            messageHUB.logStatusPercentage('Capturando imagens do usuário', sampleNumber, 10)

            if sampleNumber > 10 :
                break
        else :
            break

    db.insertNewUser(iId, sName)
