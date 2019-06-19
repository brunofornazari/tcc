import os
import time
import threading

import facialRecognition.deteccao_captura as detector
import speech_module.speechRecognition as speech
import utils.libs.db as db

if os.environ['ENVTYPE'] != 'DEV' : import integration.PIR as PIR

import utils.libs.logger as logger



from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

import utils.libs.messageHUB as messageHUB

app = Flask(__name__, root_path='public/')
app.config['SECRET_KEY'] = 'SOME_KEY'
socketio = SocketIO(app)

@app.route('/')
def mainPage():
    return render_template('index.html')

@socketio.on('message')
def handleMessage():
    emit('message', messageHUB.getMessages())
    print('message hub', messageHUB.getMessages())
    print('event called')

def startServer():
    socketio.run(app)

def main() :

    while(True):
        if os.environ['ENVTYPE'] != 'DEV' :
            bSensorCapture = PIR.detect()
        else :
            bSensorCapture = True

        if bSensorCapture == True :
            userId = detector.getUserFromCamera()
            user = db.getUserData(userId)
            logger.log('Usuário detectado: ' + str(user[0]))

            response = 1

            while response == 1:
                response = speech.startRecognizing()

            if response == 0:
                exit(0)
            else:
                responseIntents = response['entities']['intent']
                #TODO: trabalhar os intents pela confiabilidade
                responseMetadata = responseIntents[0]['metadata']
                responseValue = responseIntents[0]['value']

                #TODO: trabalhar as possibilidades e libs integradas pelo responseValue
        else :
            logger.log('nenhum usuário detectado')
            time.sleep(5)

if __name__ == '__main__' :
    threadMain = threading.Thread(target=main)
    threadServer = threading.Thread(target=startServer)

    threadServer.start()
    time.sleep(3)
    threadMain.start()