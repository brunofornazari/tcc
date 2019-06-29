import speech_recognition as sr
import utils.libs.logger as logger
import utils.config.constants as constants
import utils.libs.utils as util

def startRecognizing():
    r = sr.Recognizer()
    mic = sr.Microphone()

    try:
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


def get_intention(response):
    if response is not None and util.check_attribute(response, 'entities') and util.check_attribute(response['entities'], 'intent'):
        intents = response['entities']['intent']
        for intent in intents:
            return intent['value'], intent['confidence']
    else:
        return '', 0


def get_values(response):
    result = {}
    if response is not None and response['entities'] and response['entities']:
        intents = response['entities']

        for intent in intents:
            result[intent] = {"value" : intents[intent][0]['value'], "confidence" : intents[intent][0]['confidence']}

    return result


def wait_command(keep_execution, callback):

    while keep_execution:
        response = startRecognizing()
        logger.log('Processando...')
        intention, confidence = get_intention(response)
        if confidence > 0.9:
            if intention == 'start_command':
                keep_listening = 1
                while keep_listening == 1 and keep_execution == 1:
                    logger.log('O que posso fazer por você?')
                    command = startRecognizing()
                    command_result = get_values(command)
                    if util.check_attribute(command_result, 'intent') == True:
                        command_result_intention = command_result['intent']
                    else :
                        logger.log('Não entendi o que quis dizer, poderia repetir?')
                        pass

                    if command_result_intention['confidence'] > 0.7 and command_result_intention['value'] != 'stop_command':
                        keep_listening = 0
                        callback(command_result)
                    elif command_result_intention['confidence'] > 0.9 and command_result_intention['value'] == 'stop_command':
                        keep_listening = 0
                        logger.log('Até mais!')
                    else:
                        logger.log('Não entendi o que quis dizer, poderia repetir?')
