import time

import RPi.GPIO as GPIO

from hardware_constants import *

from pyfingerprint.pyfingerprint import PyFingerprint


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(MOTORDRIVER_INPUT1, GPIO.OUT)
GPIO.setup(MOTORDRIVER_INPUT2, GPIO.OUT)
GPIO.setup(MOTORDRIVER_INPUT3, GPIO.OUT)
GPIO.setup(MOTORDRIVER_INPUT4, GPIO.OUT)

GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)

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


while True:
    setLEDColor(1, 0, 0)

    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')
    except Exception as e:
        print('The fingerprint sensor could not be initialized: ' + str(e))
        exit(1)

    print("Waiting for finger...")

    try:
        while not f.readImage():
            pass
    except KeyboardInterrupt:
        print("Received keyboard interrupt, goodbye. :')")
        GPIO.cleanup()
        exit(0)

    f.convertImage(0x01)

    fingerprintPosition, fingerprintAccuracy = f.searchTemplate()

    if fingerprintPosition == -1 or fingerprintAccuracy < 80:
        print("No match found")

        for i in range(3):
            setLEDColor(1, 0, 0)
            time.sleep(0.25)
            setLEDColor(0, 0, 0)
            time.sleep(0.25)
        continue
    else:
        print(f"Found template at {fingerprintPosition} with accuracy score {fingerprintAccuracy}")

    del f   # turn off fingerprint sensor to save power for motor

    # open, wait, close lock
    setLEDColor(0, 1, 0)            # green color

    motorClockwise(LATCH_CYCLE_COUNT)
    time.sleep(3)
    motorCounterclockwise(LATCH_CYCLE_COUNT-20)

    setMotorStep(0, 0, 0, 0)        # don't burn out the motor waiting for fingerprints

GPIO.cleanup()
