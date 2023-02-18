import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2
# import tensorflow as tf
from PIL import Image
import time
import sys

sys.path.insert(0, '../Devboard/GPIO')

from VideoThreading import VideoGet, CountsPerSec, putIterationsPerSec 
from carControl import Drive, SERVO, Distance, Estimate_Time
from camera_input import camera_input


def carInit(Ena=32,In1=15,In2=16,Enb=33,In3=18,In4=22, Angle=0):
    # Initialize the motor
    Drive1 = Drive(Ena,In1,In2,Enb,In3,In4)


def LoadModel(weights='yolov5s'):
    return torch.hub.load("ultralytics/yolov5", f'{weights}')


def getUploadedClass(uploadedimage, weights='yolov5m'):
    model = LoadModel(weights=weights)
    '''RETURN THE DOMINANT CLASS'''
    imageModel = model(np.array(Image.open(uploadedimage)))
    # Checking the 80% threshold
    preds = imageModel.pred[0].numpy()
    print(imageModel.pandas())
    if preds[0][-2] <= 0.8:
        return 'Bring the Image to focus'
    else:
        print(imageModel.names[preds[0][-1]])
        return preds[0][-1]   


def model_detection(image_class, frame):
    pred_class = dict()
    count = 0
    model = LoadModel()
                
    results = model(frame)

    for pred in results.pred[0].numpy():
        if pred[-1] >= 0.7 and pred[-2] == image_class:
            count += 1
            return 'inframe'

            if count > 1:
                '''There is more than one target object within object return the nearest one'''
        elif pred[-1] <= 0.8 or pred[-2] != image_class:
            '''rotate the car'''
        else:
            '''return no image within range'''
            return camera_input()
        
        

        
        
        

