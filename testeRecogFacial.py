import facialRecognition.deteccao_captura as detector

if __name__ == '__main__' :
    print('executando teste v1.8')
    user = detector.getUserFromCamera()
    print('Usuário identificado:', user)