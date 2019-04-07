import facialRecognition.deteccao_captura as detector
import utils.libs.logger as logger


def main() :
    bSensorCapture = True

    if bSensorCapture == True :
        userId = detector.getUserFromCamera()
        logger.log('Usuário detectado: ' + userId)


if __name__ == '__main__' :
    main()