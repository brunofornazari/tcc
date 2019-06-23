from facialRecognition import faceCapture, facial_trainer
from utils.libs import logger
from time import sleep

logger.log('Iniciando processo de criação de usuário')
sleep(2)
logger.log('Insira um nome para o usuário')
sName = input()
logger.log('Ok, {}! Vamos iniciar a captura!'.format(sName))
faceCapture.captureNewFace(sName)
logger.log('Captura concluída! Iniciando atualização do sistema de reconhecimento')
facial_trainer.startTraining()
logger.log('Processo concluído!');


