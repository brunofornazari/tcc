import os

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/public'
app = Flask(__name__, root_path=dir_path)
app.config['SECRET_KEY'] = 'SOME_KEY'
socketio = SocketIO(app)

@app.route('/')
def mainPage():
    return render_template('index.html')

def startServer():
    socketio.run(app)


#if __name__ == '__main__':
#    socketio.run(app)