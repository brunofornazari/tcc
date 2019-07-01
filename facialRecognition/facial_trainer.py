"""
facial_trainer.py

Facial_Trainer.py é responsável por fazer o treinamento facial, reconhecendo e armazenando as caracteristicas faciais e cada 
usuário. Porém, por utilizar o HOG, ele só é capaz de treinar uma face por vez e em uma posição estática de perfíl. Caso as 
imagens retiradas não respeitem estas características, ele finaliza o processo sem finalizá-lo.
"""

import os
import glob
import _pickle as cPickle
import dlib
import cv2
import numpy as np

# Inicia o treinamento facial
def startTraining(messageHUB) :
    detectorFace = dlib.get_frontal_face_detector()
    detectorPontos = dlib.shape_predictor("resources/shape_predictor_68_face_landmarks.dat")
    reconhecimentoFacial = dlib.face_recognition_model_v1("resources/dlib_face_recognition_resnet_model_v1.dat")

    # Indicia as imagens para realizar o treinamento
    indice = {}
    idx = 0
    descritoresFaciais = None
    arquivos = glob.glob(os.path.join("dataset/", "*.jpg"))

    messageHUB.addMessage('Inicializando processo de atualização do banco de imagens...')

    # Realiza o processamento das imagens para detecção de características
    for arquivo in arquivos :
        messageHUB.logStatusPercentage('Processando arquivos', (idx + 1), len(arquivos))
        imagem = cv2.imread(arquivo)
        facesDetectadas = detectorFace(imagem, 1)
        numeroFacesDetectadas = len(facesDetectadas)
        # Ocorre quando encontra mais e uma face
        if numeroFacesDetectadas > 1 :
            messageHUB.logError("Há mais de uma face na imagem {}".format(arquivo))
            exit(0)
        # Ocorre quando não encontra uma face
        elif numeroFacesDetectadas < 1 :
            messageHUB.logError("Nenhuma face encontrada no arquivo {}".format(arquivo))
            exit(0)

        # Inicia o processo de detecção e armazenamento de caracteristicas da face
        for face in facesDetectadas :
            pontosFaciais = detectorPontos(imagem, face)
            descritorFacial = reconhecimentoFacial.compute_face_descriptor(imagem, pontosFaciais)

            listaDescritorFacial = [df for df in descritorFacial]

            npArrayDescritorFacial = np.asarray(listaDescritorFacial, dtype=np.float64)

            npArrayDescritorFacial = npArrayDescritorFacial[np.newaxis, :]

            if descritoresFaciais is None :
                descritoresFaciais = npArrayDescritorFacial
            else :
                descritoresFaciais = np.concatenate((descritoresFaciais, npArrayDescritorFacial), axis=0)

            indice[idx] = arquivo
            idx += 1

    # Realiza o armazenamento da face no determinado perfíl
    np.save("resources/descritores_captura.npy", descritoresFaciais)
    with open("resources/indices_captura.pickle", 'wb') as f :
        cPickle.dump(indice, f)

    messageHUB.addMessage('Processo de atualização do banco de imagens finalizado com sucesso!');
