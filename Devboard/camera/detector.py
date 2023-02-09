import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2
# import tensorflow as tf
from PIL import Image
import time

def LoadModel(weights='yolov5s'):
    return torch.hub.load("ultralytics/yolov5", f'{weights}')

def getUploadedClass(uploadedimage, weights='yolov5m.pt'):
    model = LoadModel()
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


def model_detection(uploadedimage):
    pred_class = dict()
    image_class = getUploadedClass(uploadedimage=uploadedimage)
    count = 0

    cap = cv2.VideoCapture(cv2.CAP_V4L2)

    # # # # Live streaming for inferencing the model
    while cap.isOpened():

        model = LoadModel()
        ret, frame = cap.read()
        
        start = time.time()

        results =model(frame)

        for pred in results.pred[0].numpy():
                if pred[-1] >= 0.8 and pred[-2] == image_class:
                    
                    end = time.time()
                    total_time = end - start
                    fps = 1/total_time
                    cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
                    # re, buffer = cv2.imencode('.jpg', np.squeeze(results.render()))
                    # frame = buffer.tobytes()
                    cv2.imshow('OpenCV Feed', np.squeeze(results.render()))

                    count += 1
                    '''Get position of the image and the rotation'''
                    if count > 1:
                        '''There is more than one target object within object return the nearest one'''
                elif pred[-1] <= 0.8 or pred[-2] != image_class:
                    '''rotate the car'''
                else:
                    '''return no image within range'''
        
        end = time.time()
        total_time = end - start
        fps = 1/total_time
        cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
        
        re, buffer = cv2.imencode('.jpg', np.squeeze(results.render()))
        frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

