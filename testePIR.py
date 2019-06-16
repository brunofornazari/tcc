import RPi.GPIO as GPIO
import time
print("initializing teste")
GPIO.setmode(GPIO.BCM)
print("mode set")
#GPIO.setwarnings(False)

pir_sensor = 11 #GPIO pin 21

GPIO.setup(pir_sensor, GPIO.IN, GPIO.PUD_DOWN)

current_state = 0

while True:
    try:
        time.sleep(0.1)
        current_state = GPIO.input(pir_sensor)
        if current_state == 1:
          print("GPIO pin %s is %s" % (pir_sensor, current_state)) # motion detected
          print("LED is ON")
          time.sleep(2)
          print("LED is OFF")
          time.sleep(4)
    except KeyboardInterrupt:
        GPIO.cleanup()