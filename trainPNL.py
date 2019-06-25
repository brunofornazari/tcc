import speech_module.speechRecognition as srlib
import utils.libs.logger as logger


def main():
    srlib.wait_command(exibe_dados)


def exibe_dados(intent, confidence):
    logger.log('intenção {} com {}% de confiança de estar correto!'.format(intent, confidence*100))


if __name__ == '__main__' :
    main()