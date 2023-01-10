import tensorflow as tf
import cv2
import numpy as np
import mediapipe as mp
from mediapipe_functs import mediapipe_detection, draw_styled_landmarks, extract_keypoints
import os

# Loading saved test points
X_test = np.load('x_test.npy')
y_test = np.load('y_test.npy')

# SAVED_MODEL_PATH 
TFLITE_FILE_PATH = 'action5.tflite'

# Loading the tensorflow model
interpreter = tf.lite.Interpreter(model_path=TFLITE_FILE_PATH)

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Resize to initial form for predictions
# interpreter.resize_tensor_input(input_details[0]['index'], (18, 30,126))
# interpreter.resize_tensor_input(output_details[0]['index'], (18, 3))
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

'''
Input Shape: [ 18  30 126]
Input Type: <class 'numpy.float32'>
Output Shape: [18  3]
Output Type: <class 'numpy.float32'>
'''

test_imgs_numpy = np.array(X_test, dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], test_imgs_numpy)
interpreter.invoke()
tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])
print(tflite_model_predictions)

mp_holistic = mp.solutions.holistic # holistic model
mp_drawing = mp.solutions.drawing_utils # drawing utilities
actions = np.array(['come', 'left', 'right'])


colors = [(245,117,16), (117,245,16), (16,117,245)]
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
    return output_frame

# 1. New detection variables
sequence = []
sentence = []
threshold = 0.8

cap = cv2.VideoCapture(0)
# Set mediapipe model 

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():

        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        print(results)
        
        # Draw landmarks
        draw_styled_landmarks(image, results)
        
        # 2. Prediction logic
        keypoints = extract_keypoints(results)
#         sequence.insert(0,keypoints)
#         sequence = sequence[:30]
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30:
              res

