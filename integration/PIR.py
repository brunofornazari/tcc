"""
PIR.py

PIR.py é responsável por fazer a requisição do acionamento e captura do recebimento de sinal. Ele utiliza de GPIOs para fazer 
este gerenciamento, assim conseguindo ser chamado por outras classes e métodos quando necessário que o periférico seja acionado 
e/ou ficar no aguardo de alguma identificação e sinal.
"""

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


