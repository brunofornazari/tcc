from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

import utils.libs.messageHUB as messageHUB

app = Flask(__name__, root_path='public/')
app.config['SECRET_KEY'] = 'SOME_KEY'
socketio = SocketIO(app)

@app.route('/')
def mainPage():
    return render_template('index.html')

@socketio.on('connect')
def handleMessage():
    messageHUB.addMessage('teste')
    emit('message', messageHUB.getMessages())
    print('message hub', messageHUB.getMessages())

def startServer():
    socketio.run(app)

#if __name__ == '__main__':
#    socketio.run(app)