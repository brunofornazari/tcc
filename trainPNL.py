import speech_module.speechRecognition as srlib
import utils.libs.logger as logger

def main():
    response = srlib.startRecognizing()
    if response == 0 :
        exit()
    else :
        responseIntents = response['entities']['intent']
        # TODO: trabalhar os intents pela confiabilidade
        logger.log('evento concluído, intent recebida: {}'.format(responseIntents))


if __name__ == '__main__' :
    main()