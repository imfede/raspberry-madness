#!/usr/bin/python3

import sys
import time
import RPi.GPIO as GPIO
import json

pin = 22
buttonpin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup( pin, GPIO.OUT)
GPIO.setup( buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP )

def play(tune, tempo):
    speed = 60 / tempo
    p = GPIO.PWM( pin, 0.5)
    p.start(1)
    for note in tune:
        p.ChangeFrequency( note[0] )
        t = time.time()
        stopt = note[1]*speed - 0.01
        while (time.time() - t) < (stopt):
            if not GPIO.input( buttonpin ):
                return False
            time.sleep( 0.05 )
    p.stop()
    return True

def getTune(filename):
    with open(filename, 'r') as jfile:
        data = json.load( jfile )
        return data['melody']

def getTempo(filename):
    with open(filename, 'r') as jfile:
        data = json.load( jfile )
        return data['tempo']

try:
    while play( getTune('melody.json'), getTempo('melody.json')):
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
