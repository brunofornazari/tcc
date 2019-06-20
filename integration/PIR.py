import RPi.GPIO as GPIO


class PIR:
    pir_sensor = 11
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pir_sensor, GPIO.IN, GPIO.PUD_DOWN)

    def __init__(self, callback):
        self._signal = 0
        self._callback = callback

    def main(self):
        pass

    def motion(self):
        self._signal = GPIO.input(pir_sensor)
        if self._signal:
            print("motion!")
        else:
            print("no motion")
        self._callback(self._signal)

    def getState(self):
        return self._signal

    GPIO.add_event_detect(pir_sensor, GPIO.BOTH, callback=motion)
