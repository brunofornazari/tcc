import speech_recognition as sr
import utils.libs.logger as logger
import utils.config.constants as constants

def startRecognizing():
    r = sr.Recognizer()
    mic = sr.Microphone()

    logger.log('Diga, em que posso ajudar')
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            logger.log('Trabalhando nisso...')
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