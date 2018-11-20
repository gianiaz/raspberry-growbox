#!/usr/bin/env python
import time
import serial
from led import Led
import RPi.GPIO as GPIO
import re
from aws import aws
ser = 0
ledActivity = Led(11, 50)
ledStatus = Led(13,500)
compiledRegex = re.compile('\[growbox\](.*)\[\/growbox\]')

temperature = 0
humidity = 0
is_day = 0
hygrometer1 = 0
hygrometer2 = 0


def setUp():
    GPIO.setmode(GPIO.BOARD)

    ledStatus.setUp()
    ledStatus.powerOn()
    ledActivity.setUp()

    # seriale
    global ser
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    ledActivity.blink(3)


def loop():
    data_str = ''
    while True:
        if ser.inWaiting:
            data_str = data_str + ser.read(ser.inWaiting()).decode('ascii')
            if data_str.find('[growbox]') != -1 and data_str.find('[/growbox]') != -1:
                analyze(data_str)
                data_str = ''
            time.sleep(0.01)

        ledActivity.updateStatus()
        awsSender.updateStatus(temperature, humidity, is_day, hygrometer1, hygrometer2)

def analyze(string_from_serial):
    print "Message received: --"+ string_from_serial+"--"
    result = compiledRegex.search(string_from_serial)
    if result is not None:
        global temperature
        global humidity
        global s_day
        global hygrometer1
        global hygrometer2

        data = result.group(1).split('|')
        temperature = data[0]
        humidity = data[1]
        is_day = 1
        hygrometer1 = data[3]
        hygrometer2 = data[4]

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
