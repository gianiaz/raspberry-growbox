from datetime import datetime
import urllib2
class aws:
    def __init__(self):
        self.lastAction = self.timestampMillisec64()
        self.bounceTime = 300000; # five minutes

    def setUrl(self, url):
        self.url = url

    def setBounceTime(self, bounceTime):
        self.bounceTime = int(bounceTime) * 1000

    def timestampMillisec64(self):
        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

    def updateStatus(self, temperature, humidity, is_day, hygrometer1, hygrometer2, led):
        if (self.lastAction + self.bounceTime) < self.timestampMillisec64():
            # send data
            url = self.url + '&temperature='+str(temperature)+"&humidity="+str(humidity)+"&is_day="+str(is_day)+"&hygrometer1="+str(hygrometer1)+"&hygrometer2="+str(hygrometer2)
            print "[AWS] Sending to "+ url
            response = urllib2.urlopen(url);
            # print response.read();
            led.blink(2);
            self.lastAction = self.timestampMillisec64()
