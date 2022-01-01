import time

import RPi.GPIO as GPIO

from hardware_constants import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)

def setColor(r, g, b):
    GPIO.output(LED_RED, r)
    GPIO.output(LED_GREEN, g)
    GPIO.output(LED_BLUE, b)

setColor(1, 0, 0)

time.sleep(3)

GPIO.cleanup()
