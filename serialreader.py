import re
import time
import serial
import datetime

class serialReader:

    def __init__(self, bounceTimeSeconds, port):
        self.serial = serial.Serial(
                port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        self.bounceTimeSeconds = bounceTimeSeconds
        self.lastAction = time.time()
        self.lecture = ''
        self.regex = '\[growbox\](.*)\[\/growbox\]'
        self.maxLines = 10


        a = 'hfjkladhfadfhdajfhadfdafh'
        b = '[growbox]30|45|0|95|14[\/growbox\]'
        print re.match(self.regex, a)
        print re.match(self.regex, b)

    def listen(self, regex):
        if(self.lastAction + self.bounceTimeSeconds < time.time()):
            self.lastAction = time.time()
            self.compiledRegex = re.compile(regex)
            line = ''
            count = 0
            while(line == ''):
                data = self.serial.readline();
                result = self.compiledRegex.match(data)
                if(result):
                    line = result.group(1)
                if(count == self.maxLines):
                    line = 'timeout'
            return line
        else:
            return None
