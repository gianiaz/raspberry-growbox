from datetime import datetime
import RPi.GPIO as GPIO

class Led:
    def __init__(self, pin, bounceTime):
        self.pin = pin
        self.lastAction = self.timestampMillisec64()
        self.powered = False
        self.bounceTime = bounceTime
        self.blinkStart = 0;
        self.blinking = False
        self.blinkingDuration = 0

    def timestampMillisec64(self):
        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

    def setUp(self):
        GPIO.setup(self.pin, GPIO.OUT)  # Set LedPin's mode is output

    def powerOn(self):
        GPIO.output(self.pin, GPIO.HIGH)  # led off
        self.powered = True
        print '...led on'

    def powerOff(self):
        GPIO.output(self.pin, GPIO.LOW)  # led on
        self.powered = False
        print 'led off...'


    def toggle(self):
        self.lastAction = self.timestampMillisec64()
        if self.powered:
            self.powerOff()
        else:
            self.powerOn()


    def updateStatus(self):
        # if self.blinking and :
        #     self.blinking = False
        #     self.powerOff()
        #     print("Stop blinking")

        if self.blinking:
            if self.lastAction + self.bounceTime < self.timestampMillisec64():
                self.toggle()
            if self.blinkStart + (self.blinkingDuration * 1000) < self.timestampMillisec64():
                self.blinking = False
                self.powerOff()

    def blink(self, duration):
            self.blinking = True
            print("Start blinking")
            self.blinkingDuration = duration
            self.blinkStart = self.timestampMillisec64()


    def destroy():
        GPIO.cleanup()  # Release resource
