import os
import threading
if os.environ.get('ENVTYPE') != 'DEV' : import facialRecognition.deteccao_captura as detector
import speech_module.speechRecognition as speech
import utils.libs.logger as logger
import utils.libs.db as db
import utils.config.constants as constants
import pyowm
from datetime import datetime, timedelta
from newsapi import NewsApiClient
if os.environ.get('ENVTYPE') != 'DEV' : from integration.PIR import PIR


owm = pyowm.OWM(constants.PYOWM_KEY)
news_intents = {
    'noticias_politica' : {
        'query' : 'politica'
    },
    'noticias_esportes' : {
        'category' : 'sports'
    },
    'noticias_economia' : {
        'category' : 'business'
    },
    'noticias_gerais' : {
        'category' : 'general'
    }
}

newsapi = NewsApiClient(api_key=constants.NEWS_KEY)

def main() :
    PIR(mirror)
    #mirror(1)


def mirror(bSensorCapture):

    if bSensorCapture:
        userId = detector.getUserFromCamera()
        #userId = 'Visitante'
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
    elif intent['intent']['value'] in news_intents :
        intention = intent['intent']['value']
        result = ''

        if check_attribute(news_intents[intention], 'query') :
            query = news_intents[intention]['query']
        else :
            query = ''

        if check_attribute(news_intents[intention], 'category') :
            category = news_intents[intention]['category']
        else :
            category = 'general'

        top_headlines = newsapi.get_top_headlines(
                                                  q=query,
                                                  category=category,
                                                  language='pt',
                                                  page_size=5,
                                                  country='br')
        for content in top_headlines['articles']:
            result += '<div class="news-content"><div class="part-width"><img src="{}" width="300" /></div><div class="part-width"><h1>{}</h1></div><div class="break"></div></div>'.format(content['urlToImage'], content['title'])
        logger.log(result)
    else:
        logger.log('Essa ação não está disponível no momento :/')


def check_attribute(object, property):
    for attribute in object:
        if attribute == property: return True

    return False


