import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
import time


# graph_def = tf.compat.v1.GraphDef()
# labels = []

# # These are set to the default names from exported models, update as needed.
# filename = "ssd_mobilenet_v2_taco_2018_03_29.pb"
# labels_filename = "labelmap.pbtxt"

# # Import the TF graph
# with tf.io.gfile.GFile(filename, 'rb') as f:
#     graph_def.ParseFromString(f.read())
#     tf.import_graph_def(graph_def, name='')

# # Create a list of labels.
# with open(labels_filename, 'rt') as lf:
#     for l in lf:
#         labels.append(l.strip())




model = torch.hub.load("ultralytics/yolov5", 'yolov5s')
# model = tf.saved_model.load('ssd_mobilenet_v2_taco_2018_03_29.engine')
# model = torch.load('cpu.pt', map_location=torch.device('cpu'))
# model = modelling(model_name)
# model.load_state_dict(state)
# TFLITE_FILE_PATH = 'model.tflite'

# # # Loading the tensorflow model
# interpreter = tflite.lite.Interpreter(model_path=TFLITE_FILE_PATH)

# # # Get input and output tensors.
# interpreter.allocate_tensors()
# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()
# interpreter.resize_tensor_input(input_details[0]['index'],[1, 3, 320, 320])
# interpreter.allocate_tensors()
# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()
# print(input_details[0]['shape'])
# # print('\n\n\n\n\n\n\n')
# print(output_details)

# '''Frame shape (480, 640, 3)'''
# '''Input Details shape [ 32,   3, 320, 320] '''
# '''Output Details shape [  32, 6300,   15]'''

cap = cv2.VideoCapture(1)


# # # # Live streaming for inferencing the model
while cap.isOpened():
    ret, frame = cap.read()
    start = time.time()
#     frame2 = cv2.resize(frame, (320,320))
# # #     # Make detections
#     test = np.expand_dims(np.array(frame2, dtype=np.float32), axis=0)
#     interpreter.set_tensor(input_details[0]['index'], test)
#     interpreter.invoke()

#     res = interpreter.get_tensor(output_details[0]['index'])
    results =model(frame)
# #     print(test)
# #     print(type(test))

# #     print(test.shape)
    end = time.time()
    total_time = end - start
    fps = 1/total_time
    cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
    cv2.imshow('Yolo Model', np.squeeze(results.render()))

    if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

cap.release()
cv2.destroyAllWindows()


# while True:
#     ret, frame  = cap.read()
    
#     # convert the frames to numpy array
#     image_np = np.array(frame)
#     # Convert to tensors and increase dimensions
#     input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

    