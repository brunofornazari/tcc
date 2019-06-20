from integration.PIR import PIR
from signal import pause

def tryPIR(signal):
    print('we gotta a', signal)

_PIR = PIR(tryPIR)
pause()

