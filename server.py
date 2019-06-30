"""
server.py

Server.py é responsável por manter o servidor de aplicação ativo, recebendo e enviando dados a cada usuário
conectado. O servidor de aplicação é baseado em flask e seu protocolo de comunicação é o de websockets via
socket.io. Os recursos relacionados a web estão localizados e são servidor através do package 'public',
subdividido em dois outros packages, static, responsável por manter salvas as imagens, códigos javascript e
CSS necessários para a interface de usuário e funcionamento correto da aplicação pelo front-end e templates,
onde é mantido os códigos HTML.

Para a aplicação iniciar de forma correta, é gerido um código randômico de 128 bits afim de que possa ser
garantida segurança de tráfego de dados, gerando uma nova chave de acesso a cada inicialização. Após definir
onde estarão os recursos estáticos e iniciar o flask, é iniciado o socketio que irá gerenciar o fluxo de chamadas
através de websockets.

Algumas rotas são pré definidas, conforme descrito a seguir, e após a definição das rotas, uma instância do messageHUB
para que a comunicação entre app.py e client sejam tratadas da forma correta. Para o envio de mensagens ao cliente de
forma simples e genérica, foi construído o método broadcast, que é inserido como um observer do messageHUB e, através
de uma lista de usuários previamente definidas e os handles de conexão e desconexão, consegue encaminhar as mensagens
a cada sessão de usuário conectado.

Rotas:

 - /
    Direciona ao index.html e é a página padrão onde o usuário recebe feed constante de cada log gerado e enviado através
    do messageHUB para os sockets.

 - /newUser
    Direciona ao createUser.html onde o client poderá iniciar o fluxo de criação de usuário.

Handlers:

 - on -> connect
    Ao conectar, o client tem sua sessão adicionada a lista 'clients' onde estará apto a receber broadcasts.

 - on -> disconnect
    Ao sair da página (desconectar), o client tem sua sessão removida da lista 'clients' e deixará de receber broadcasts
    gerados pelo programa.

 - on -> register-user
    O handler é responsável por, ao receber a requisição, iniciar o fluxo de captura, criação e treinamento da ia para um
    novo usuário.

Functions
 - startServer()
    Inicia o servidor flask com socketio.

 - broadcast(message String, event_emition String)
    Itera pela lista 'clients' e envia a cada sessão gravada na lista uma determinada mensagem. O tipo de mensagem enviada
    pode variar, conforme o parâmetro event_emition é preenchido e emite uma mensagem ao evento específico, porém, caso
    não for definido, assumirá o valor padrão 'message'.
"""

import os
import random

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from utils.libs.messageHUB import MessageHUB
from facialRecognition import faceCapture, facial_trainer
from time import sleep

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/public'
app = Flask(__name__, root_path=dir_path)
app.config['SECRET_KEY'] = random.getrandbits(128)
socketio = SocketIO(app)
clients = []

__messageHUB__ = 0


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
    faceCapture.captureNewFace(nome_usuario, messageHUB)
    facial_trainer.startTraining(messageHUB)
    broadcastMessage('Usuario criado com sucesso!', 'user-creation-complete')


def startServer():
    socketio.run(app)


def broadcastMessage(sMessage, event_emition='message'):
    for client in clients:
        socketio.emit(event_emition, sMessage, room=client)


messageHUB = MessageHUB()
messageHUB.bind_callback(broadcastMessage)

if __name__ == '__main__' :
    pass

