import os
import time

import facialRecognition.deteccao_captura as detector
import speech_module.speechRecognition as speech
import utils.libs.logger as logger
import utils.libs.db as db

if os.environ['ENVTYPE'] != 'DEV' : import integration.PIR as PIR

def main() :

    while(True):
        if os.environ['ENVTYPE'] != 'DEV' :
            bSensorCapture = PIR.detect()
        else :
            bSensorCapture = False

        if bSensorCapture is True :
            userId = detector.getUserFromCamera()
            user = db.getUserData(userId)
            logger.log('Usuário detectado: ' + str(user[0]))

            response = 1

            while response == 1:
                response = speech.startRecognizing()

            if response == 0:
                exit(0)
            else:
                responseIntents = response['entities']['intent']
                #TODO: trabalhar os intents pela confiabilidade
                responseMetadata = responseIntents[0]['metadata']
                responseValue = responseIntents[0]['value']

                #TODO: trabalhar as possibilidades e libs integradas pelo responseValue
        else :
            logger.log('nenhum usuário detectado')
            time.sleep(5)