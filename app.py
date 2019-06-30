"""
app.py

App.py é responsável por gerenciar o fluxo de eventos que identifica, reconhece, ouve e responde as requisições de usuários
a frente do espelho. Os fluxo de eventos é definido conforme comentado abaixo:

 -> Para cada mudança de status do PIR conectado via GPIO pela raspberry pi, uma função callback 'mirror(Boolean bSensorCapture)' é
 invocada. Caso o ENV_TYPE=DEV, o valor padrão do bSensorCapture é 1 (nível lógico alto), que dispara os demais eventos.

 -> Quando a mudança do PIR for para estado alto (1), o método getUserFromCamera(), da biblioteca 'facialRecognition.deteccao_captura'
 é invocado e espera como retorno um id de usuário de banco ou 'Visitante', em caso onde não for possível reconhecer um usuário em particular.

 -> Caso um usuário seja reconhecido e seu id de banco seja o retorno da chamada, é usado o método getUserData(int userId) para buscar no
 banco de dados os demais dados de usuário através da biblioteca utils.libs.db.

 -> O período é definido através da hora local do sistema afim de determinar qual seria a melhor forma de abordar o usuário

 -> Uma mensagem então é enviada ao usuário para que saiba que o espelho está a disposição aguardando um comando.

 -> Uma nova thread é iniciada para cuidar de escutar e receber comandos do usuário através do método wait_command(Boolean bSensorCapture, function call_intent)
 da biblioteca speech_module.speechRecognition. O estado do sensor em observer é passado ao método para que este saiba quando parar a thread ou ficar inativo quando
 o usuário não for mais identificado pelo sensor PIR. call_intent é a função que deve ser invocada uma vez que o usuário faça um comando e que deverá tratar
 as requisições conforme a intent identificada.

 Funções e métodos

  - main()
    Inicia a classe PIR e define a função mirror(Boolean bSensorCaptrura) como callback.

  - mirror(Boolean bSensorCapture)
    Responsável por invocar os métodos de identificação, reconhecimento do perfil e escutar os comandos dos usuários.

  - call_intent(dict Intent)
     Dependendo da intent, call_intent irá realizar uma ação e responder ao usuário com os dados solicitados, sendo definido pelo escopo do projeto as
     seguintes intents programas:

        * previsao_tempo - Identifica através da intent o quando e onde para solicitar ao pyowm, via request Server-to-Server, a previsão do tempo
        nas condições estabelecidas.

        * noticias_esportes/noticias_politica/noticias_economia/notivias_gerais - Identifica, dependendo do tipo de notícia, a busca (query) e categoria
        (category) a qual ela se encaixaria para que uma request Server-to-Server seja realizada ao newsapi afim de responder ao usuário os tipos de
        notícias solicitadas.

"""

import os
import threading
import facialRecognition.deteccao_captura as detector
import speech_module.speechRecognition as speech
import utils.libs.logger as logger
import utils.libs.db as db
import utils.config.constants as constants
import pyowm
from datetime import datetime, timedelta
from newsapi import NewsApiClient
import codecs
if os.environ.get('ENVTYPE') != 'DEV' : from integration.PIR import PIR

#Inicia o pyowm com a chave API cadastrada
owm = pyowm.OWM(constants.PYOWM_KEY)

#Cria lista das intents de notícias e suas respectivas queries e categories disponíveis
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

#Inicia a newsapi com a chave API vinculada a conta criada.
newsapi = NewsApiClient(api_key=constants.NEWS_KEY)


def main() :
    if os.environ.get('ENVTYPE') != 'DEV':
        PIR(mirror)
    else :
        mirror(1)




def mirror(bSensorCapture):

    if bSensorCapture:
        userId = detector.getUserFromCamera()
        if userId != 'Visitante':
            print(userId)
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
        templateHTML = codecs.open('public/templates/previsaoTemplate.html').read()
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

        logger.log(templateHTML.format(when.day, when.month, when.year, where, temperature['temp'], temperature['temp_min'], temperature['temp_max']))
    elif intent['intent']['value'] in news_intents :
        intention = intent['intent']['value']
        result = ''
        templateHTML = codecs.open('public/templates/noticiasHeader.html').read()
        templateItem = codecs.open('public/templates/noticiasItem.html').read()

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
                                                  page_size=3,
                                                  country='br')
        for content in top_headlines['articles']:
            news_title = content['title']
            slice_item = slice(0, 80)

            if len(news_title):
                news_title = news_title[slice_item]
                news_title += '...'

            result += templateItem.format(content['urlToImage'], news_title)
        logger.log(templateHTML.format(result))
    else:
        logger.log('Essa ação não está disponível no momento :/')


def check_attribute(object, property):
    for attribute in object:
        if attribute == property: return True

    return False

if __name__ == '__main__' :
    pass
