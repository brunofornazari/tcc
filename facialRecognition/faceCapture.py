"""
faceCapture.py

FaceCapture.py é responsável por fazer a captura da face suas respectivas características. São tiradas apenas 10 fotos
do rosto para este comparativo, pois o beneficio de resultado não era maior que 3% para uma quantia maior do que isto enquanto
o processo ficava cada vez mais pesado conforme a quantia de imagens aumentasse.
"""

import cv2
import dlib
import utils.libs.db as db
from integration.camera import Camera

def captureNewFace(sName, messageHUB) :
    # Inicia a câmera
    detectorFace = dlib.get_frontal_face_detector()
    cam = Camera()
    cam.start()

    iId = db.getNextId()
    sampleNumber = 0

    # Inicia a captura imagens
    while sampleNumber < 10:
        img = cam.read()
        faces = detectorFace(img, 1)

        # Gera um contador para o armazenamento das 10 imagens
        for face in faces:
            if sampleNumber < 10:

                # Incrementa o contador de imagens
                # Armazena em quatro variaveis os valores das caracteristicas em um rosto
                # Retorna qual imagem foi capturada
                sampleNumber = sampleNumber+1
                e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
                cv2.imwrite("dataset/" + str(iId) + "." + str(sampleNumber) + ".jpg", img)
                cv2.rectangle(img, (e, t), (d, b), (0, 255, 255), 2)
                cv2.waitKey(100)
            messageHUB.logStatusPercentage('Capturando imagens do usuário', sampleNumber, 10)

            # Finaliza o fluxo de captura
            if sampleNumber >= 10 :
                break

    # Registra o como usuário a face no banco de dados
    db.insertNewUser(iId, sName)
