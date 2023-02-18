import tensorflow as tflite
# import tflite_runtime.interpreter as tflite
import cv2
import numpy as np
import mediapipe as mp
from mediapipe_functs import mediapipe_detection, draw_styled_landmarks, extract_keypoints
import os

# SAVED_MODEL_PATH 
TFLITE_FILE_PATH = r'C:\Users\Austin\Desktop\Agent\Car movements\CMS\Devboard\camera\action5.tflite'

# Loading the tensorflow model
interpreter = tflite.lite.Interpreter(model_path=TFLITE_FILE_PATH)

# Get input and output tensors.
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


mp_holistic = mp.solutions.holistic # holistic model
mp_drawing = mp.solutions.drawing_utils # drawing utilities
actions = np.array(['come', 'left', 'right'])
action2 = np.array(['standby', 'come', 'left', 'right'])


colors = [(245,117,16), (117,245,16), (16,117,245)]
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
    return output_frame

# 1. New detection variables


def camera_inference():
    sequence = []
    sentence = []
    predictions = []
    threshold = 0.5
    cap = cv2.VideoCapture(0)
# Set mediapipe model 
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
        # Read feed
            ret, frame = cap.read()
            if not ret:
                break
            else:
            # Make detections
                image, results = mediapipe_detection(frame, holistic)
            # print(results)
            
            # Draw landmarks
                draw_styled_landmarks(image, results)
            
            # 2. Prediction logic
                keypoints = extract_keypoints(results)
                sequence.append(keypoints)
                sequence = sequence[-30:]
            
                if len(sequence) == 30:
                    test = np.expand_dims(np.array(sequence, dtype=np.float32), axis=0)
                    interpreter.set_tensor(input_details[0]['index'], test)
                    interpreter.invoke()
            
                    res = interpreter.get_tensor(output_details[0]['index'])[0]
                # res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    # print(res)
                # print(np.argmax(tflite_model_predictions))
                    # print(actions[np.argmax(res)])
                    predictions.append(np.argmax(res))
                
                
            #3. Viz logic
                    if np.unique(predictions[-10:])[0]==np.argmax(res): 
                        if res[np.argmax(res)] > threshold: 
                            if len(sentence) > 0: 
                                if actions[np.argmax(res)] != sentence[-1]:
                                    sentence.append(actions[np.argmax(res)])
                            else:
                                sentence.append(actions[np.argmax(res)])

                    if len(sentence) > 5: 
                        sentence = sentence[-5:]

                # Viz probabilities
                    image = prob_viz(res, actions, image, colors)
                
                cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
                cv2.putText(image, ' '.join(sentence), (3,30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Show to screen
                re, buff = cv2.imencode('.jpg', image)
                image = buff.tobytes()

            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
# camera_inference()


# camera(interpreter, input_details, output_details, mp_holistic, actions, colors, prob_viz, sequence, sentence, predictions, threshold)