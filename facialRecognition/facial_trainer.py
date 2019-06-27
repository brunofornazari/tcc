import os
import glob
import _pickle as cPickle
import dlib
import cv2
import numpy as np

def startTraining(messageHUB) :
    detectorFace = dlib.get_frontal_face_detector()
    detectorPontos = dlib.shape_predictor("resources/shape_predictor_68_face_landmarks.dat")
    reconhecimentoFacial = dlib.face_recognition_model_v1("resources/dlib_face_recognition_resnet_model_v1.dat")

    indice = {}
    idx = 0
    descritoresFaciais = None
    arquivos = glob.glob(os.path.join("dataset/", "*.jpg"))

    messageHUB.addMessage('Inicializando processo de atualização do banco de imagens...')

    for arquivo in arquivos :
        messageHUB.logStatusPercentage('Processando arquivos', (idx + 1), len(arquivos))
        imagem = cv2.imread(arquivo)
        facesDetectadas = detectorFace(imagem, 1)
        numeroFacesDetectadas = len(facesDetectadas)
        if numeroFacesDetectadas > 1 :
            messageHUB.logError("Há mais de uma face na imagem {}".format(arquivo))
            exit(0)
        elif numeroFacesDetectadas < 1 :
            messageHUB.logError("Nenhuma face encontrada no arquivo {}".format(arquivo))
            exit(0)

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

    np.save("resources/descritores_captura.npy", descritoresFaciais)
    with open("resources/indices_captura.pickle", 'wb') as f :
        cPickle.dump(indice, f)

    messageHUB.log('Processo de atualização do banco de imagens finalizado com sucesso!');