import facialRecognition.deteccao_captura as detector

if __name__ == '__main__' :
    user = detector.getUserFromCamera()
    print('Usuário identificado:', user)