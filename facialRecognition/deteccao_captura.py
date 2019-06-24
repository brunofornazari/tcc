import os
import dlib
import cv2
import numpy as np
import imutils
import utils.libs.logger as logger
from integration.camera import Camera


def main() :
    pass


def getUserFromCamera() :
    detectorFace = dlib.get_frontal_face_detector()
    detectorPontos = dlib.shape_predictor(os.path.abspath("resources/shape_predictor_68_face_landmarks.dat"))
    reconhecimentoFacial = dlib.face_recognition_model_v1("resources/dlib_face_recognition_resnet_model_v1.dat")
    indices = np.load("resources/indices_captura.pickle", allow_pickle=True)
    descritoresFaciais = np.load("resources/descritores_captura.npy", allow_pickle=True)
    limiar = 0.5
    camera = Camera()
    stream = camera.capture()
    userId = -1

    logger.log('Detectando usuário...')

    while userId == -1 :
        for (i, f) in enumerate(stream):
            frame = f.array
            frame = imutils.resize(frame, width=400)
            facesDetectadas = detectorFace(frame, 2)
            for face in facesDetectadas :
                e, t, d, b = (int(face.left()), int(face.top()), int(face.right()), int(face.bottom()))
                pontosFaciais = detectorPontos(frame, face)
                descritorFacial = reconhecimentoFacial.compute_face_descriptor(frame, pontosFaciais)

                listaDescritorFacial = [fd for fd in descritorFacial]
                npArrayDescritorFacial = np.asarray(listaDescritorFacial, dtype=np.float64)
                npArrayDescritorFacial = npArrayDescritorFacial[np.newaxis, :]

                distancias = np.linalg.norm(npArrayDescritorFacial - descritoresFaciais, axis=1)
                minimo = np.argmin(distancias)
                distanciaMinima = distancias[minimo]

                if distanciaMinima <= limiar :
                    if os.environ.get('ENVTYPE') == 'DEV' :
                        userId = os.path.split(indices[minimo])[1].split(".")[0]

                    else :
                        print('indice', minimo, indices)
                        userId = os.path.split(indices[minimo])[1].split('\\')[1].split(".")[0]
                    logger.log('Usuário detectado')
                else :
                    userId = 'Visitante'

                camera.stop()
                if userId != 0:
                    break
            camera.stop()
            if(userId != 0):
                break
        #todo - Caso de exceção onde não foi possível encontrar nenhum user cadastrado
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    print('returning')
    return userId


if __name__ == '__main__' :
    main()
