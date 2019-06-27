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

    def logStatus(self, sMessage, iCurrent, iMax):
        message = sMessage + ' - ' + str(iCurrent) + '/' + str(iMax)
        sys.stdout.write('\r')
        sys.stdout.write(message)
        sys.stdout.flush()
        self.addMessage(message)


    def logStatusPercentage(self, sMessage, iCurrent, iMax):
        currentPercentage = (iCurrent / iMax) * 100
        message = sMessage + ' - ' + '{0:.2f}%'.format(currentPercentage)
        sys.stdout.write('\r')
        sys.stdout.write(message)
        sys.stdout.flush()
        self.addMessage(message)

    def logError(self, sMessage):
        print('\n\nError: {}'.format(sMessage) + '\n\n')
        self.addMessage('<span class="error">Oops..{} <br> :(</span>'.format(sMessage))


    def bind_callback(self, callback):
        self._observers.append(callback)

    def getMessages(self):
        p = self._messageHUB.copy()
        print(self._messageHUB)
        self._messageHUB = ''
        return p