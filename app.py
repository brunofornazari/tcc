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
    # Caso o ENV_TYPE=DEV, considera-se sinal alto de presença sempre, se não, ativa-se a PIR e observa-se seu valor
    if os.environ.get('ENVTYPE') != 'DEV':
        PIR(mirror)
    else :
        mirror(1)




def mirror(bSensorCapture):
    # Caso o sensor PIR envie sinal alto, iniciado o fluxo
    if bSensorCapture:
        # Inicia o fluxo para identificação de index de usuário
        userId = detector.getUserFromCamera()
        # Caso o usuário tenha valor diferente de 'Visitante', seus dados são obtidos através do banco de dados, do contrário
        # o fluxo inicia considerando um usuário padrão 'Visitante'
        if userId != 'Visitante':
            user = db.getUserData(userId)
        else:
            user = ['Visitante']

        # A hora local do sistema operacional é obtida para que possa definir como seria a melhor forma de cumprimentar
        # o usuário
        now = datetime.now()
        at_noon = now.replace(hour=12)
        at_night = now.replace(hour=18)

        if now <= at_noon :
            greeting = 'Bom dia'
        elif now >= at_night:
            greeting = 'Boa noite'
        else:
            greeting = 'Boa tarde'

        # Então é enviado o cumprimento gerado ao usuário
        logger.log('{}, {}'.format(greeting, str(user[0])))

        # Caso haja dados de usuário, como é esperado, inicia-se a thread de captura e tratamento de comando pelo
        # microfone. O valor do sensor e uma função callback 'call_intent' é enviado para a thread para que possa
        # tratar devidamente as ações conforme as ações de usuário
        if len(user) > 0:
            thread_speech = threading.Thread(target=speech.wait_command, args=[bSensorCapture, call_intent])
            thread_speech.start()




def call_intent(intent):
    # Caso o valor de retorno da wit.ai seja uma intent cujo valor seja 'previsao_tempo', é iniciado o tratamento para
    # a ação de recuperar os dados de previsão metereológica conforme as informações obtidas.
    if intent['intent']['value'] == 'previsao_tempo':
        # Carrega o tempalte HTML que será, depois, retornado ao usuário com os dados
        templateHTML = codecs.open('public/templates/previsaoTemplate.html').read()

        # Verifica-se se há na intent um atributo 'location', se houver, o valor desse atributo é considerado para o local
        # de onde deseja-se saber a previsão metereológico, se não houver, é considerado um valor padrão 'São Paulo'
        if check_attribute(intent, 'location'):
            where = intent['location']['value']
        else:
            where = 'São Paulo'

        # Verifica-se se há na intent um atributo 'datetime', se houver, o valor desse atributo é considerado para quando
        # deseja-se saber a previsão metereológico, se não houver, é considerado um valor padrão do dia atual da requisição
        if check_attribute(intent, 'datetime'):
            slice_object = slice(0, 10)
            when = datetime.strptime(intent['datetime']['value'][slice_object], '%Y-%m-%d')
            when = when + timedelta(days=0, hours=24)
        else:
            when = datetime.now() + timedelta(days=0, hours=12)

        # Determina, para o owm, o local e data de quando se deseja obter a previsão metereológica
        forecaster = owm.three_hours_forecast(where)
        weather = forecaster.get_weather_at(when)
        # Configura-se que o valor da temperatura deverá sem em graus Célcius
        temperature = weather.get_temperature('celsius')

        # Os valores de local, hora e valores de temperatura são formatados no template HTML e é enviado ao client
        logger.log(templateHTML.format(when.day, when.month, when.year, where, temperature['temp'], temperature['temp_min'], temperature['temp_max']))
    elif intent['intent']['value'] in news_intents :
        # Caso o valor da intent enteja na lista de tipos de noticias disponíveis, inicia-se o fluxo de tratameto para busca e retorno de notícias

        # O valor da intent é atribuido a uma variável para que seu acesso seja facilitado
        intention = intent['intent']['value']

        # É criado uma variável result em string vazia que é onde serão concatenados os templates e valores ao decorrer do código
        result = ''

        # Carregado os templates html, dois templates são usados, um que é agregado ao outro, o noticiasHeader define a estrutura da lista de notícias,
        # o noticiasItem define a estrutura de cada item (notícia) e como será demonstrada
        templateHTML = codecs.open('public/templates/noticiasHeader.html').read()
        templateItem = codecs.open('public/templates/noticiasItem.html').read()

        # Caso haja, na configuração do item da lista em que a intent se encontra, um atributo query, este valor da intent é
        # definido em uma variável 'query'. Caso não houver, um valor '' é atribuído
        if check_attribute(news_intents[intention], 'query') :
            query = news_intents[intention]['query']
        else :
            query = ''

        # Caso haja, na configuração do item da lista em que a intent se encontra, um atributo category, este valor é
        # definido em uma variável 'category'. Caso não houver, um valor 'general' é atribuído
        if check_attribute(news_intents[intention], 'category') :
            category = news_intents[intention]['category']
        else :
            category = 'general'

        # É atribuído as variáveis query e category para a chamada das notícias via newsapi e seu resultado em uma variável
        # top_headlines
        top_headlines = newsapi.get_top_headlines(
                                                  q=query,
                                                  category=category,
                                                  language='pt',
                                                  page_size=3,
                                                  country='br')

        # Para cada notícia retornada, é separado o título e a utl de imagem que, em seguida é concatenada a variável
        # result
        for content in top_headlines['articles']:
            news_title = content['title']
            slice_item = slice(0, 80)

            if len(news_title):
                news_title = news_title[slice_item]
                news_title += '...'

            result += templateItem.format(content['urlToImage'], news_title)
        # Após iterar sobre as notícias, limitadas à 3 (devido ao tamanho da tela), as informações são enviadas ao usuário.
        logger.log(templateHTML.format(result))
    else:
        # Caso a intent não esteja dentro das opções válidas, é avisado ao usuário que a ação não está disponível
        logger.log('Essa ação não está disponível no momento :/')


def check_attribute(object, property):
    # A função check_attribute é responsável por avaliar se a propriedade passada faz parte do objeto em questão
    # para isso, itera-se por cada propriedade disponível no objeto e compara a propriedade passada como parâmetro
    # caso haja, o loop é interrompido e returna-se True. Se ao final da iteração não houver retornado ao usuário,
    # retorna-se False.
    for attribute in object:
        if attribute == property: return True

    return False

# Caso o app.py seja iniciado diretamente, o fluxo não é iniciado.
if __name__ == '__main__' :
    pass
