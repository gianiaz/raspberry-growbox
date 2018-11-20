from datetime import datetime
import urllib2
class aws:
    def __init__(self, url, bounceTime):
        self.url = url
        self.lastAction = self.timestampMillisec64()
        self.bounceTime = bounceTime * 1000

    def timestampMillisec64(self):
        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

    def updateStatus(self, temperature, humidity, is_day, hygrometer1, hygrometer2):
        if self.lastAction + self.bounceTime < self.timestampMillisec64():
            # send data
            url = self.url + '&temperature='+str(temperature)+"&humidity="+str(humidity)+"&is_day="+str(is_day)+"&hygrometer1="+str(hygrometer1)+"&hygrometer2="+str(hygrometer2)
            print "[AWS] Sending to "+ url
            urllib2.urlopen(url);

            self.lastAction = self.timestampMillisec64()

