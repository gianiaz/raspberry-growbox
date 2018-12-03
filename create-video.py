#!/usr/bin/env python

import sys,getopt,os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
import shutil

def main(argv):
    dir = ''
    try:
        opts, args = getopt.getopt(argv, "hd:", ["dir"])
    except getopt.GetoptError:
        print 'create-video.py -d <directory>'
        sys.exit(2)
    for opt, arg in opts:
        if(opt == '-h'):
            print 'create-video.py -d <directory>'
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir = arg.rstrip('/')


    images = [img for img in os.listdir(dir) if img.endswith(".jpg")]
    if(len(images) == 0):
        print 'Directory "'+dir+'" does not contains images'
        sys.exit()


    print 'Directory "'+dir+'" contains '+str(len(images))+' images'
    print 'Processing...'

    for image in images:
        img = Image.open(dir+ "/" + image)
        extrema = img.convert("L").getextrema()
        if(extrema[1] < 50):
            dest = dir + "/discarded"
            if(not os.path.exists(dest)):
                os.mkdir(dest);
                print("Created directory "+ dest)
            print "Discarding image "+image
            os.rename(dir+"/"+ image, dir+"/discarded/"+ image)
        else:
            dest = dir + "/temp"
            if(not os.path.exists(dest)):
                os.mkdir(dest);
                print("Created directory "+ dest)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("./UbuntuMono-R.ttf", 50)
            timestamp = int(os.path.splitext(image)[0])
            draw.rectangle([2010, 1810, 2500, 1900], fill=(0,0,0,128));
            draw.text((2030, 1830),datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y - %H:%M'),(255,255,255),font=font)
            img.save(dest+'/'+image)
            print "Processed image for "+datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y - %H:%M')

    command = 'ffmpeg -r 24 -pattern_type glob -i "'+dir+'/temp/*.jpg" -s hd1080 -vcodec libx264 '+dir+'/'+dir.split('/').pop()+'.mp4'
    os.system(command)

    shutil.rmtree(dir+'/temp/')
    if(os.path.exists(dir+'/discarded/')):
        shutil.rmtree(dir+'/discarded/')

if __name__ == "__main__":
   main(sys.argv[1:])
