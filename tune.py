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

def play( filename ):
    speed = 60 / getTempo( filename )
    tuning = getTuning(filename)
    inter = getInter( filename )
    p = GPIO.PWM( pin, 0.5)
    for note in getTune( filename ):
        if( note[0] > 10 ):
            p.start(1)
            p.ChangeFrequency( note[0]*tuning )
        t = time.time()
        stopt = note[1]*speed - 0.01
        while (time.time() - t) < (stopt):
            if not GPIO.input( buttonpin ):
                return False
            time.sleep( 0.05 )
        if( note[0] > 10 ):
            p.stop()
        time.sleep( inter )
    return True

def getInter(filename):
    with open(filename, 'r') as jfile:
        data = json.load( jfile )
        return data['inter']

def getTuning(filename):
    with open(filename, 'r') as jfile:
        data = json.load( jfile )
        return data['tuning']

def getTune(filename):
    with open(filename, 'r') as jfile:
        data = json.load( jfile )
        return data['melody']

def getTempo(filename):
    with open(filename, 'r') as jfile:
        data = json.load( jfile )
        return data['tempo']

try:
    while play( sys.argv[1] ):
        time.sleep(1)
except KeyboardInterrupt:
    pass # do nothing
finally:
    GPIO.cleanup()
