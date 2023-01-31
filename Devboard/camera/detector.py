import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
import time


model = torch.hub.load("ultralytics/yolov5", 'yolov5s')

def model_detection():
    cap = cv2.VideoCapture(0)


    # # # # Live streaming for inferencing the model
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        else:
            start = time.time()

            results =model(frame)
            
            end = time.time()
            total_time = end - start
            fps = 1/total_time
            cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
            re, buffer = cv2.imencode('.jpg', np.squeeze(results.render()))
            frame = buffer.tobytes()
            
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
