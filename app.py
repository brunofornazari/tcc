import os
import threading
import facialRecognition.deteccao_captura as detector
import speech_module.speechRecognition as speech
import utils.libs.logger as logger
import utils.libs.db as db
import datetime
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

        now = datetime.now()
        at_noon = now.replace(hour=12)
        at_night = now.replace(hour=18)

        if now <= at_noon :
            greeting = 'Bom dia'
        elif now >= at_night:
            greeting = 'Boa noite'
        else:
            greeting = 'Boa tarde'

        logger.log('{}, {}'.format(greeting, str(user[0])))

        if len(user) > 0:
            thread_speech = threading.Thread(target=speech.wait_command, args=[bSensorCapture, call_intents])
            thread_speech.start()


def call_intents(response):
    logger.log('{} - {}%'.format(response['intent']['value'], response['intent']['confidence']))

