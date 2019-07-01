***
deteccao_captura.py

Detecção_Captura.py é responsável por fazer a detecção e identificação a face através das caracteristicas capturadas nas imagens 
retiradas pelo faceCapture.py. Para isto, ele segue uma rota de fluxo:
    - Inicia o processo de detecção de face nas imagens capturadas;
    - Ele realiza até 10 tentativas de identificação;
    - Caso identifique, ele retorna informando a qual perfil pertence a face;
    - Caso não identifique as caracteristicas em nenhum dos perfils, ele retorna informando que é o perfil de um visitante;
***

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
    # Inicia a detecção
    detectorFace = dlib.get_frontal_face_detector()
    detectorPontos = dlib.shape_predictor(os.path.abspath("resources/shape_predictor_68_face_landmarks.dat"))
    reconhecimentoFacial = dlib.face_recognition_model_v1("resources/dlib_face_recognition_resnet_model_v1.dat")
    indices = np.load("resources/indices_captura.pickle", allow_pickle=True)
    descritoresFaciais = np.load("resources/descritores_captura.npy", allow_pickle=True)
    limiar = 0.5
    cam = Camera()
    cam.start()
    userId = -1

    logger.log('Detectando usuário...')
    tentativas_conexao = 0
    # Estabelece a quantia de tentativas
    while userId == -1 or tentativas_conexao < 10:
        imagem = cam.read()
        facesDetectadas = detectorFace(imagem, 2)
        # Detecta as características através de pontos faciais específicos
        for face in facesDetectadas:
            pontosFaciais = detectorPontos(imagem, face)

            descritorFacial = reconhecimentoFacial.compute_face_descriptor(imagem, pontosFaciais)
            # Faz a busca e comparação com perfís cadastrados
            if descritorFacial != None:
                listaDescritorFacial = [fd for fd in descritorFacial]
                npArrayDescritorFacial = np.asarray(listaDescritorFacial, dtype=np.float64)
                npArrayDescritorFacial = npArrayDescritorFacial[np.newaxis, :]

                distancias = np.linalg.norm(npArrayDescritorFacial - descritoresFaciais, axis=1)
                minimo = np.argmin(distancias)
                distanciaMinima = distancias[minimo]
            else :
                pass
            # Retorna o perfil identificado
            if distanciaMinima <= limiar :
                userId = os.path.split(indices[minimo])[1].split(".")[0]
            else :
                userId = 'Visitante'


            if userId != -1:
                break

        if(userId != -1):
            break

        tentativas_conexao += 1
        
        # Retorna o perfíl de visitante
    if userId == -1:
        userId = 'Visitante'

    cv2.destroyAllWindows()

    return userId


if __name__ == '__main__' :
    main()
