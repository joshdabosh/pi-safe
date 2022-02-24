from flask import Flask

import time

import RPi.GPIO as GPIO

from hardware_constants import *

from pyfingerprint.pyfingerprint import PyFingerprint

def setLEDColor(r, g, b):
    GPIO.output(LED_RED, r)
    GPIO.output(LED_GREEN, g)
    GPIO.output(LED_BLUE, b)

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


lock = 0
app = Flask(__name__)

@app.route("/asdffdsa123")
def open():
    global lock
    if lock:
        return "-1"
    lock = 1
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(MOTORDRIVER_INPUT1, GPIO.OUT)
    GPIO.setup(MOTORDRIVER_INPUT2, GPIO.OUT)
    GPIO.setup(MOTORDRIVER_INPUT3, GPIO.OUT)
    GPIO.setup(MOTORDRIVER_INPUT4, GPIO.OUT)

    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_BLUE, GPIO.OUT)
    
    motorClockwise(LATCH_CYCLE_COUNT)
    time.sleep(3)

    motorCounterclockwise(LATCH_CYCLE_COUNT)

    setMotorStep(0, 0, 0, 0)        # don't burn out the motor waiting for fingerprints

    GPIO.cleanup()
    lock=0

    return "1"

app.run(host="0.0.0.0")
