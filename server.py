import os
import random

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from utils.libs.messageHUB import MessageHUB
#from facialRecognition import faceCapture, facial_trainer
from time import sleep
import testeLogger

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/public'
app = Flask(__name__, root_path=dir_path)
app.config['SECRET_KEY'] = random.getrandbits(128)
socketio = SocketIO(app)
clients = []


@app.route('/')
def mainPage():
    return render_template('index.html')


@app.route('/newUser')
def createuser():
    return render_template('createUser.html')


@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)

@socketio.on('register-user')
def handle_createUser(nome_usuario):
    broadcastMessage('Iniciando processo de captura de imagens de novo usuário')
    sleep(2)
    #faceCapture.captureNewFace(nome_usuario)
    #facial_trainer.startTraining()
    testeLogger.teste()
    broadcastMessage('Usuario criado com sucesso!', 'user-creation-complete')



def startServer():
    socketio.run(app)


def broadcastMessage(sMessage, event_emition='message'):
    for client in clients:
        socketio.emit(event_emition, sMessage, room=client)


messageHUB = MessageHUB()
messageHUB.bind_callback(broadcastMessage)

