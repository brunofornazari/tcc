import sys
from server import messageHUB

def log(sMessage, emition_type='message') :
    messageHUB.addMessage(sMessage, emition_type)

def logStatus(sMessage, iCurrent, iMax) :
    message = sMessage + ' - ' + str(iCurrent) + '/' + str(iMax)
    sys.stdout.write('\r')
    sys.stdout.write(message)
    sys.stdout.flush()
    messageHUB.addMessage(message)


def logStatusPercentage(sMessage, iCurrent, iMax) :
    currentPercentage = (iCurrent/iMax)*100
    message = sMessage + ' - ' + '{0:.2f}%'.format(currentPercentage)
    sys.stdout.write('\r')
    sys.stdout.write(message)
    sys.stdout.flush()
    messageHUB.addMessage(message)

def logError(sMessage) :
    messageHUB.addMessage('<span class="error">Oops..{} <br> :(</span>'.format(sMessage))

def logDebug(sMessage) :
    print('\n\nDebug: {}'.format(sMessage) + '\n\n')