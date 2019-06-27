from time import sleep

def teste(messageHUB):
    messageHUB.addMessage('processando')
    sleep(5)
    messageHUB.addMessage('processado!')