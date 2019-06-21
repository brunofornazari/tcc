#from server import socketio
#from flask_socketio import emit


class MessageHUB:

    def __init__(self):
        self._messageHUB = ''
        self._observers = []

    def __str__(self):
        return self._messageHUB

    def addMessage(self, sMessage):
        self._messageHUB = sMessage
        for callback in self._observers:
            callback(self._messageHUB)

    def bind_callback(self, callback):
        self._observers.append(callback)

    def getMessages(self):
        p = self._messageHUB.copy()
        print(self._messageHUB)
        self._messageHUB = ''
        return p