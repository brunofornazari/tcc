import speech_module.speechRecognition as srlib
import utils.libs.logger as logger
from datetime import datetime, timedelta

import pyowm

owm = pyowm.OWM('48250140b550af15b1537f212d815013')

def main():
    srlib.wait_command(1, call_intent)


def exibe_dados(intent):
    logger.log('intenção {} com {}% de confiança de estar correto!'.format(intent['intent']['value'], intent['intent']['confidence']))
    if hasattr(intent, 'location'):
        logger.log('a localização passado é {}'.format(intent['location']['value']))
    if hasattr(intent, 'datetime'):
        logger.log('a data resultado é {}'.format(intent['datetime']['value']))


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
            when = datetime.now() + timedelta(days=0, hours=12)

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



if __name__ == '__main__' :
    main()