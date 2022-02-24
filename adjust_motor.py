import time

import RPi.GPIO as GPIO

from hardware_constants import *


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(MOTORDRIVER_INPUT1, GPIO.OUT)
GPIO.setup(MOTORDRIVER_INPUT2, GPIO.OUT)
GPIO.setup(MOTORDRIVER_INPUT3, GPIO.OUT)
GPIO.setup(MOTORDRIVER_INPUT4, GPIO.OUT)

GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)


def setMotorStep(w1, w2, w3, w4):
    GPIO.output(MOTORDRIVER_INPUT1, w1)
    GPIO.output(MOTORDRIVER_INPUT2, w2)
    GPIO.output(MOTORDRIVER_INPUT3, w3)
    GPIO.output(MOTORDRIVER_INPUT4, w4)


def motorClockwise(cycleCount):
    for i in range(cycleCount):
        for coilsPower in MOTOR_CYCLE:
            setMotorStep(*coilsPower)
            time.sleep(0.001)


def motorCounterclockwise(cycleCount):
    for i in range(cycleCount):
        for coilsPower in MOTOR_CYCLE[::-1]:
            setMotorStep(*coilsPower)
            time.sleep(0.001)


while True:
    try:
        x = input(": ")
    except:
        GPIO.cleanup()
    if x.strip() == "i":
        motorCounterclockwise(10)
    elif x.strip() == "d":
        motorClockwise(10)
    else:
        continue

GPIO.cleanup()
