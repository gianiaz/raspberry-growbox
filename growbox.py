#!/usr/bin/env python
import ConfigParser
import time
import serial
from aws import aws
import re
from serialreader import serialReader
from led import Led
import RPi.GPIO as GPIO

awsSender = aws();
ser = serialReader(10, '/dev/ttyACM0')
temperature = 0
humidity = 0
is_day = 0
hygrometer1 = 0
hygrometer2 = 0
ledActivity = Led(11, 50)
ledStatus = Led(13,500)


def setUp():
    global config
    config = ConfigParser.ConfigParser()
    try:
        config.read('config.ini')
        url = config.get('aws', 'url')+"/?token="+config.get('aws', 'token')
        bounceTimeSeconds = config.get('aws', 'bounceTimeSeconds');
        awsSender.setUrl(url)
        awsSender.setBounceTime(bounceTimeSeconds)
    except ConfigParser.NoSectionError:
        print "Missing config file, copy default file config.ini.dist to config.ini and modify with your needs"

    GPIO.setmode(GPIO.BOARD)

    ledStatus.setUp()
    ledStatus.powerOn()
    ledActivity.setUp()

def loop():
    while True:
        global temperature
        global humidity
        global is_day
        global hygrometer1
        global hygrometer2

        line = ser.listen('\[growbox\](.*)\[\/growbox\]')
        if(line != None):
            data = line.split('|')
            temperature = data[0]
            humidity = data[1]
            is_day = data[2]
            hygrometer1 = data[3]
            hygrometer2 = data[4]

        awsSender.updateStatus(temperature, humidity, is_day, hygrometer1, hygrometer2, ledActivity)
        ledActivity.updateStatus()

def destroy():
    ledActivity.destroy()
    ledStatus.destroy()
    GPIO.cleanup() # cleanup all GPIO

if __name__ == '__main__':  # Program start from here
    setUp()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
