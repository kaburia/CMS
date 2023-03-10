import cv2
import time
import torch
import numpy as np
import sys
import concurrent.futures
from math import pi
import datetime

# import tensorflow as tf
from PIL import Image
import time
import os
import numpy as np

import argparse
import time
# from matplotlib import cm

from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

sys.path.insert(0, '/home/pi/Desktop/CMS/Devboard/GPIO')
from carControl import Drive, SERVO, Distance, Estimate_Time
from VideoThreading import VideoGet, CountsPerSec, putIterationsPerSec

# model = torch.hub.load("ultralytics/yolov5", 'yolov5s')
Drive1 = Drive(12,6,5, 13, 26, 16)
# # open camera
# # cv2.CAP_V4L2
speed = 100

# Get the image class
'''Utilizing the function uploadclass'''
image_class = 'person'

# an approximate distance hardcoded 
'''replace with distance from ultrasonic sensor'''
distance = 3

# without encoder assumption 100% is 200rpm
DutyCycle = 100 # 1DutyCycle == 2rpm

# Revs
revs = DutyCycle * 1.4

# Diameter of the wheel 7cm
circumference = pi*0.07 # in metres 1 rev == 0.22m

# this depends on the dutycycle
velocity = (circumference * revs) / 60

# From the distance get the time in seconds
runtime = distance/velocity

def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red')
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill='red')

model = '/home/pi/Desktop/CMS/Devboard/camera/v1.tflite'
labels = read_label_file('/home/pi/Desktop/CMS/Devboard/camera/label.txt')
interpreter = make_interpreter(model)
interpreter.allocate_tensors()

def camera_input():
    video_getter = VideoGet(cv2.CAP_V4L2).start()
    cps = CountsPerSec().start()
    while True:
        frame_capture = 0
        
        # Get Frame
        # print(f'Moving Forward: {speed}')
        # Drive1.moveB(speed)

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        img = Image.fromarray(frame)
        start_time = time.time()
        _, scale = common.set_resized_input(
        interpreter, img.size, lambda size: img.resize(size, Image.ANTIALIAS))

        for _ in range(3):
            start = time.perf_counter()
            interpreter.invoke()
            inference_time = time.perf_counter() - start
            objs = detect.get_objects(interpreter, 0.5, scale)
            print('%.2f ms' % (inference_time * 1000))

        print('-------RESULTS--------')
        if not objs:
            print('No objects detected')
        for obj in objs:
            print(labels.get(obj.id, obj.id))
            print('  id:    ', obj.id)
            print('  score: ', obj.score)
            print('  bbox:  ', obj.bbox)
        print(objs)
        # end_time = time.time()
        # total_time = end_time - start_time
        # fps = 1/total_time
        
        image = img.convert('RGB')
        draw_objects(ImageDraw.Draw(image), objs, labels)
        
        if objs:
            model_class = labels.get(objs[0].id, objs[0].id)
            if model_class.lower() == image_class.lower():
                endTime = datetime.datetime.now() + datetime.timedelta(seconds=runtime)
                while True:
                    print(f'Moving Forward, Time: {datetime.datetime.now()}')
                    Drive1.moveB(speed=DutyCycle)
                    frame = np.array(image)
                    re, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield(b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    cps.increment()
                    if datetime.datetime.now() >= endTime:
                        Drive1.STOP()
                        # Drive1.moveB(DutyCycle)
                        break
        # if obj.i

            # results = model(frame)
        # frame = np.squeeze(results.render())
        
        # cv2.imshow('OpenCV Feed', frame)
        
        frame = np.array(image)
        re, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

    

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cps.increment()
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     executor.map(camera_input)

# camera_input()
