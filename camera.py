from picamera import PiCamera
import time
from datetime import datetime
import os.path

camera = PiCamera()
camera.rotation = 180
camera.resolution = (2592,1944)
class Camera:
    def __init__(self, bounceTime):
        self.bounceTimeSeconds = bounceTime
        self.lastAction = time.time()

    def setBasePath(self, basePath):
        self.basePath = basePath

    def updateStatus(self):
        if(self.lastAction + self.bounceTimeSeconds < time.time()):
            dest = self.basePath + str(datetime.now().isocalendar()[1])
            if(not os.path.exists(dest)):
                os.mkdir(dest);
                print "directory "+ dest + "created"

            dest += "/"+str(int(time.time()))+".jpg"
            print dest
            camera.start_preview()
            time.sleep(2)
            camera.capture(dest)
            camera.stop_preview()
