import RPi.GPIO as GPIO
import time

import utils.libs.logger as logger

GPIO.setmode(GPIO.BOARD)
pir_sensor = 11
GPIO.setup(pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
current_state = 0

def main():
    pass

def detect():
    try:
        time.sleep(0.1)

        current_state = GPIO.input(pir_sensor)

        if current_state == 0:
          time.sleep(5)
        else :
            return True
    except :
        GPIO.cleanup()

if __name__ == '__main__' :
    main()
