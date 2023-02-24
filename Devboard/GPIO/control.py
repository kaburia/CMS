from carControl import Drive, SERVO, Distance, Estimate_Time
import sys
import cv2
import time
import datetime
from math import pi

sys.path.insert(0, '/home/pi/Desktop/CMS/Devboard/camera/')
from VideoThreading import VideoGet, CountsPerSec, putIterationsPerSec
from detector import model_detection, getUploadedClass

Drive1 = Drive(32,15,16,33,18,22)

# Starting the camera
# video_getter = VideoGet().start()
# cps = CountsPerSec().start()

# Get the image class
'''Utilizing the function uploadclass'''
image_class = 'person'

# an approximate distance hardcoded 
'''replace with distance from ultrasonic sensor'''
distance = 10

# without encoder assumption 100% is 200rpm
DutyCycle = 100 # 1DutyCycle == 2rpm

# Revs
revs = DutyCycle * 2

# Diameter of the wheel 7cm
circumference = pi*0.07 # in metres 1 rev == 0.22m

# this depends on the dutycycle
velocity = (circumference * revs) / 60

# From the distance get the time in seconds
runtime = distance/velocity

def control():
    video_getter = VideoGet().start()
    cps = CountsPerSec().start()
    while True:
        frame_capture = 0
        
        # Get Frame
        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())

        # checking through the camera's lenses
        if model_detection(image_class, frame)=='inframe' and frame_capture == 0:
            endTime = datetime.datetime.now() + datetime.timedelta(seconds=runtime)
            frame_capture = 1
            while True:
                Drive1.moveF(DutyCycle)
                yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                if datetime.datetime.now() >= endTime:
                    break
            
        
        re, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

    

        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


