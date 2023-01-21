import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
cap = cv2.VideoCapture(0)

# Live streaming for inferencing the model
while cap.isOpened():
    ret, frame = cap.read()

    # Make detections
    results =model(frame)

    cv2.imshow('Yolo Model', np.squeeze(results.render()))

    if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

cap.release()
cv2.destroyAllWindows()