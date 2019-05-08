import speech_recognition as sr
import utils.libs.logger as logger

def startRecognizing():
    r = sr.Recognizer()
    mic = sr.Microphone()

    logger.log('Diga, em que posso ajudar')
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            logger.log('Trabalhando nisso...')
            return r.recognize_wit(audio_data = audio, key='DYKWSZNME4ABW3TH57O75K4XKED7EL5J', show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        logger.logError('Oops..Parece que estamos sem conexão com a internet')
        return 0
    except sr.UnknownValueError:
        # speech was unintelligible
        logger.logError('Não entendi o que disse, poderia repetir?')
        return 1