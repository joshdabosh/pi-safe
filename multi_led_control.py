import time
import itertools
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

arr = [4, 2, 1, 6, 3, 7]

for i in arr:
    setColor(i & 4, i & 2, i & 1)
    time.sleep(1)


GPIO.cleanup()
