import os
import glob
import _pickle as cPickle
import dlib
import cv2
import numpy as np
import imutils
import utils.libs.logger as logger
from imutils.video.pivideostream import PiVideoStream

def main() :
    pass


def getUserFromCamera() :
    detectorFace = dlib.get_frontal_face_detector()
    detectorPontos = dlib.shape_predictor(os.path.abspath("resources/shape_predictor_68_face_landmarks.dat"))
    reconhecimentoFacial = dlib.face_recognition_model_v1("resources/dlib_face_recognition_resnet_model_v1.dat")
    indices = np.load("resources/indices_captura.pickle", allow_pickle=True)
    descritoresFaciais = np.load("resources/descritores_captura.npy", allow_pickle=True)
    limiar = 0.5
    vs = PiVideoStream().start()
    userId = 0

    logger.log('Detectando usuário...')

    while userId == 0 :
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        cv2.imgshow("Frame", frame)
        facesDetectadas = detectorFace(frame, 2)
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
                if os.environ['ENVTYPE'] == 'DEV' :
                    nome = os.path.split(indices[minimo])[1].split(".")[0]
                else :
                    nome = os.path.split(indices[minimo])[1].split('\\')[1].split(".")[0]
                userId = nome
                logger.log('Usuário detectado')
                vs.stop()
            else :
                nome = "unknown"
                vs.stop()

        #todo - Caso de exceção onde não foi possível encontrar nenhum user cadastrado
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

    return userId


if __name__ == '__main__' :
    main()
