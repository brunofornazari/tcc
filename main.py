import facialRecognition.deteccao_captura as detector
import utils.libs.db as db

import utils.libs.logger as logger


def main() :
    bSensorCapture = True

    if bSensorCapture == True :
        userId = detector.getUserFromCamera()
        user = db.getUserData(userId)
        logger.log('Usuário detectado: ' + str(user[0]))


if __name__ == '__main__' :
    main()