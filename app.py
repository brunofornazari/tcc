import os
import threading
import facialRecognition.deteccao_captura as detector
import speech_module.speechRecognition as speech
import utils.libs.logger as logger
import utils.libs.db as db
import utils.config.constants as constants
import pyowm
from datetime import datetime, timedelta
if os.environ.get('ENVTYPE') != 'DEV' : from integration.PIR import PIR


owm = pyowm.OWM(constants.PYOWM_KEY)


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
            thread_speech = threading.Thread(target=speech.wait_command, args=[bSensorCapture, call_intent])
            thread_speech.start()


def call_intent(intent):
    if intent['intent']['value'] == 'previsao_tempo':
        if check_attribute(intent, 'location'):
            where = intent['location']['value']
        else:
            where = 'São Paulo'

        if check_attribute(intent, 'datetime'):
            slice_object = slice(0, 10)
            when = datetime.strptime(intent['datetime']['value'][slice_object], '%Y-%m-%d')
            when = when + timedelta(days=0, hours=24)
        else:
            when = datetime.now() + timedelta(days=0, hours=24)

        forecaster = owm.three_hours_forecast(where)
        weather = forecaster.get_weather_at(when)
        temperature = weather.get_temperature('celsius')

        logger.log('A previsão do tempo para o dia {}/{}/{} é de: <br> Min: {}ºC e Max: {} ºC'.format(when.day, when.month, when.year, temperature['temp_min'], temperature['temp_max']))

    else:
        logger.log('Essa ação não está disponível no momento :/')


def check_attribute(object, property):
    for attribute in object:
        if attribute == property: return True

    return False


