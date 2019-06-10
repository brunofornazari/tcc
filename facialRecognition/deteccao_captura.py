import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import dlib
import cv2
import numpy as np

import utils.libs.logger as logger

def main() :
    pass

def getUserFromCamera() :
    detectorFace = dlib.get_frontal_face_detector()
    detectorPontos = dlib.shape_predictor(os.path.abspath("resources/shape_predictor_68_face_landmarks.dat"))
    reconhecimentoFacial = dlib.face_recognition_model_v1("resources/dlib_face_recognition_resnet_model_v1.dat")
    indices = np.load("resources/indices_captura.pickle", allow_pickle=True)
    descritoresFaciais = np.load("resources/descritores_captura.npy", allow_pickle=True)
    limiar = 0.5
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 32
    userId = 0

    logger.log('Detectando usuário...')

    while userId == 0 :
        time.sleep(2)
        imagem = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(imagem, 'bgr')
        cv2.imshow('img', imagem)
        facesDetectadas = detectorFace(imagem, 2)
        for face in facesDetectadas :
            e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
            pontosFaciais = detectorPontos(imagem, face)
            descritorFacial = reconhecimentoFacial.compute_face_descriptor(imagem, pontosFaciais)

            listaDescritorFacial = [fd for fd in descritorFacial]
            npArrayDescritorFacial = np.asarray(listaDescritorFacial, dtype=np.float64)
            npArrayDescritorFacial = npArrayDescritorFacial[np.newaxis, :]

            distancias = np.linalg.norm(npArrayDescritorFacial - descritoresFaciais, axis=1)
            minimo = np.argmin(distancias)
            distanciaMinima = distancias[minimo]

            if distanciaMinima <= limiar :
                nome = os.path.split(indices[minimo])[1].split(".")[0]
                userId = nome
                logger.log('Usuário detectado')
            else :
                nome = "unknown"

        #todo - Caso de exceção onde não foi possível encontrar nenhum user cadastrado
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

    return userId

if __name__ == '__main__' :
    main()
