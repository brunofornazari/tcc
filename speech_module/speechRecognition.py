"""
speechRecognition.py

SpeechRecognition.py é responsável por iniciar a biblioteca speech_recognition junto do microfone para realizar a captura de uma 
frase e envio para a Wit.ai processar este aúdio e retornar com o valor requisitado. Ele realiza isto seguindo ma rota de fluxo:
    - Primeiro ele ajusta os dados que forem capturados através de uma instancia para reconhecimento de ruídos ambiente;
    - Depois disso, ele escuta as frases ditas e absorvidas pelo microfone;
    - Ele envia para o Wit.ai para transformação em texto;
    - Recebe a intent do Wit.ai como um objeto;
    - Extrai o metadado e valor do objeto para validar se a resposta recebida é valida:
    - Confere se a confiabiliade do objeto é maior que 80%;
        -- Caso não seja valido ou maior o que 80%, ele retorna pro usuário repetir a frase;
    - Envia o argumento de entrada referente ao comando solicitado.
Para seguir está rota, ele utiliza de alguns comandos que ditam quais serão os próximos processos. Sendo eles:
    - Start_command: para iniciar o fluxo de aceitar um comando
    - Stop_command: para interromper o fluxo de esperar por um comando
    - Noticias_esportes: frases que sejam pertinentes para o retorno de noticias de esportes
    - Noticias_politica: frases que sejam pertinentes para o retorno de noticias relacionada a política
    - Noticias_economia: frases que sejam pertinentes para o retorno de noticias de economia
    - Noticias_gerais: frases que sejam pertinentes para o retorno de noticias em geral
    - Previsão_tempo: frases que sejam pertinentes a questões sobre a previsão meteorológica
"""

import speech_recognition as sr
import utils.libs.logger as logger
import utils.config.constants as constants
import utils.libs.utils as util

# Inicia as funções importadas a biblioteca speech_recognition
def startRecognizing():
    r = sr.Recognizer()
    mic = sr.Microphone()

    # Inicia a captura de comandos de voz com o microfone
    try:
        # Envia para a Wit.ai a fala capturada
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            return r.recognize_wit(audio_data = audio, key=constants.WITAI_KEY, show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        logger.logError('Oops..Parece que estamos sem conexão com a internet')
        return 0
    except sr.UnknownValueError:
        # speech was unintelligible
        logger.logError('Não entendi o que disse, poderia repetir?')
        return 1
    except RuntimeError:
        logger.logError('Algo saiu errado')
        return 2

# Recebe o objeto
def get_intention(response):

    # Valida se o objeto é valido
    if response is not None and util.check_attribute(response, 'entities') and util.check_attribute(response['entities'], 'intent'):
        intents = response['entities']['intent']
        for intent in intents:
            return intent['value'], intent['confidence']
    else:
        return '', 0


    # Extrai o metadado e valor do objeto
def get_values(response):
    result = {}
    # Realiza o teste de confiabilidade
    if response is not None and isinstance(response, dict) and response['entities'] and response['entities']:
        intents = response['entities']

        for intent in intents:
            result[intent] = {"value" : intents[intent][0]['value'], "confidence" : intents[intent][0]['confidence']}

    return result


# Inicia o fluxo e reconhecimento dos comandos através da fala
def wait_command(keep_execution, callback):

    while keep_execution:
        response = startRecognizing()
        logger.log(True, 'processing')
        intention, confidence = get_intention(response)
        if confidence > 0.9:
            if intention == 'start_command':
                keep_listening = 1
                logger.log(False, 'processing')
                while keep_listening == 1 and keep_execution == 1:
                    logger.log('O que posso fazer por você?')
                    logger.log(True, 'processing')
                    command = startRecognizing()
                    logger.log(False, 'processing')
                    command_result = get_values(command)
                    command_result_intention = False
                    if util.check_attribute(command_result, 'intent') == True:
                        command_result_intention = command_result['intent']
                    else :
                        logger.log('Não entendi o que quis dizer, poderia repetir?')
                        pass

                    if command_result_intention and command_result_intention['confidence'] > 0.8 and command_result_intention['value'] != 'stop_command':
                        keep_listening = 0
                        callback(command_result)
                    elif command_result_intention and command_result_intention['confidence'] > 0.9 and command_result_intention['value'] == 'stop_command':
                        keep_listening = 0
                        logger.log('Até mais!')
                    else:
                        logger.log('Não entendi o que quis dizer, poderia repetir?')
