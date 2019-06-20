import sys
from server import messageHUB

def log(sMessage) :
    print(sMessage)
    messageHUB.addMessage(sMessage)

def logStatus(sMessage, iCurrent, iMax) :
    sys.stdout.write('\r')
    sys.stdout.write(sMessage + ' - ' + str(iCurrent) + '/' + str(iMax))
    sys.stdout.flush()


def logStatusPercentage(sMessage, iCurrent, iMax) :
    currentPercentage = (iCurrent/iMax)*100
    sys.stdout.write('\r')
    sys.stdout.write(sMessage + ' - ' + '{0:.2f}%'.format(currentPercentage))
    sys.stdout.flush()


def logError(sMessage) :
    print('\n\nError: {}'.format(sMessage) + '\n\n')

def logDebug(sMessage) :
    print('\n\nDebug: {}'.format(sMessage) + '\n\n')