import RPi.GPIO as GPIO


class PIR:


    def __init__(self, callback):
        self._signal = 0
        self._callback = callback
        self._pir_sensor = 11
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._pir_sensor, GPIO.BOTH, callback=self.motion)

    def main(self):
        pass

    def motion(self, pir_sensor):
        self._signal = GPIO.input(pir_sensor)
        self._callback(self._signal)

    def getState(self):
        return self._signal


