from picamera import PiCamera
import time
from datetime import datetime
import os.path
import requests

camera = PiCamera()
camera.rotation = 180
camera.resolution = (2592,1944)
class Camera:
    def __init__(self, bounceTime):
        self.bounceTimeSeconds = bounceTime
        self.lastAction = time.time()
        self.moduleName = '[CAMERA] '

    def setBasePath(self, basePath):
        self.basePath = basePath

    def setUrl(self, url):
        self.url = url

    def updateStatus(self, is_day):
        if(is_day and self.lastAction + self.bounceTimeSeconds < time.time()):
            dest = self.basePath + str(datetime.now().isocalendar()[1])
            if(not os.path.exists(dest)):
                os.mkdir(dest);
                print self.moduleName + "Directory "+ dest + "created"

            dest += "/"+str(int(time.time()))+".jpg"
            camera.start_preview()
            time.sleep(2)
            camera.capture(dest)
            camera.stop_preview()

            time.sleep(2)
            print "[CAMERA] Sending photo to "+self.url

            with open(dest, 'rb') as f:
                try:
                    response = requests.post(self.url, files={'last': f})
                    print self.moduleName + " Response: "+response.text
                    self.lastAction = time.time()
                except requests.exceptions.Timeout:
                    print self.moduleName + "Timeout"
                except requests.exceptions.TooManyRedirects:
                    print self.moduleName + "Too many Redirects"
                except requests.exceptions.RequestException as e:
                    print self.moduleName + "Connection failed"
