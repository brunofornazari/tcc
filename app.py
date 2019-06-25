import os
import threading
import facialRecognition.deteccao_captura as detector
import speech_module.speechRecognition as speech
import utils.libs.logger as logger
import utils.libs.db as db
if os.environ.get('ENVTYPE') != 'DEV' : from integration.PIR import PIR


def main() :
    PIR(mirror)


def mirror(bSensorCapture):

    if bSensorCapture:
        userId = detector.getUserFromCamera()
        if userId != 'Visitante':
            user = db.getUserData(userId)
        else:
            user = ['Visitante']
        # TODO: FAZER GREETINGS
        logger.log('Usuário detectado: ' + str(user[0]))
        if len(user) > 0:
            thread_speech = threading.Thread(target=speech.wait_command, args=[bSensorCapture, call_intents])
            thread_speech.start()

            # TODO: trabalhar as possibilidades e libs integradas pelo responseValue


def call_intents(intent, confidence):
    logger.log(intent, confidence)

