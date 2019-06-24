import cv2
import numpy as np
import dlib
import utils.libs.db as db
import imutils
import utils.libs.logger as logger
from integration.camera import Camera


def captureNewFace(sName) :
    detectorFace = dlib.get_frontal_face_detector()
    cam = Camera()
    stream = cam.capture()
    iId = db.getNextId()
    sampleNumber = 0

    while True :
        for (i, img) in enumerate(stream):
            frame = img.array
            frame = imutils.resize(frame, width=400)
            if sampleNumber < 10:
                faces = detectorFace(frame, 1)

                for face in faces :
                    sampleNumber = sampleNumber+1
                    e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
                    cv2.imwrite("dataset/" + str(iId) + "." + str(sampleNumber) + ".jpg", img)
                    cv2.rectangle(img, (e, t), (d, b), (0, 255, 255), 2)
                    cv2.waitKey(100)
                logger.log('Imagem ' + str(sampleNumber) + ' gravada')
                if sampleNumber > 10 :
                    break
            else :
                break
    camera.stop()
    db.insertNewUser(iId, sName)
