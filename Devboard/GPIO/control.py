from carControl import Drive, SERVO, Distance, Estimate_Time
import sys
import cv2

sys.path.insert(0, '/home/kali/Desktop/CMS/Devboard/camera/')
from VideoThreading import VideoGet, CountsPerSec, putIterationsPerSec
from detector import model_detection, getUploadedClass

Drive1 = Drive(32,15,16,33,18,22)

# Starting the camera
video_getter = VideoGet().start()
cps = CountsPerSec().start()

# Get the image class
'''Utilizing the function uploadclass'''
image_class = 'person'

while True:
    frame_capture = 0
    
    # Get Frame
    frame = video_getter.frame
    frame = putIterationsPerSec(frame, cps.countsPerSec())
    
    cv2.imshow('OpenCV Feed', frame)
    cps.increment()

    if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

    

