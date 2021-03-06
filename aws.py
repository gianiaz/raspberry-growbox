from datetime import datetime
import urllib2
import sys
import logging

class aws:
    def __init__(self):
        self.lastAction = self.timestampMillisec64()
        self.bounceTime = 300000; # five minutes
        self.logPrefix = '[AWS] ';
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG, filename="growbox.log")

    def setUrl(self, url):
        self.url = url

    def setBounceTime(self, bounceTime):
        self.bounceTime = int(bounceTime) * 1000

    def timestampMillisec64(self):
        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

    def updateStatus(self, temperature, humidity, is_day, hygrometer1, hygrometer2, fan_active, humidifier_active, led):
        if (self.lastAction + self.bounceTime) < self.timestampMillisec64():
            # send data
            try:
                url = self.url + '&temperature='+str(temperature)+"&humidity="+str(humidity)+"&is_day="+str(is_day)+"&hygrometer1="+str(hygrometer1)+"&hygrometer2="+str(hygrometer2)+"&fan_active="+str(fan_active)+"&humidifier_active="+str(humidifier_active);
                logging.info(self.logPrefix + "Sending to "+ url)
                response = urllib2.urlopen(url);
                # print response.read();
                led.blink(2);
                self.lastAction = self.timestampMillisec64()
            except urllib2.URLError:
                logging.error(self.logPrefix+ "Connection error")
            except urllib2.HTTPError:
                logging.error(self.logPrefix+ "Http Error")
