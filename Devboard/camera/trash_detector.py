'''
Inferencing a model trained on 60 classes to detect trash in an image/frame
'''

import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt
from tensorflow.python.util import compat
from tensorflow.core.protobuf import saved_model_pb2
from google.protobuf import text_format
import pprint
import json
import os
import sys
import cv2
import time

# Tensorflow object detection
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import dataset_util, label_map_util
from object_detection.protos import string_int_label_map_pb2

# initializing opencv to read usb camera
cap = cv2.VideoCapture(1)

ANNOTATIONS_FILE = 'annotations.json'
NCLASSES = 60

# Reading into the labels
with open(ANNOTATIONS_FILE) as json_file:
    data = json.load(json_file)
    
categories = data['categories']

# Building label map 

labelmap = string_int_label_map_pb2.StringIntLabelMap()
for idx,category in enumerate(categories):
    item = labelmap.item.add()
    # label map id 0 is reserved for the background label
    item.id = int(category['id'])+1
    item.name = category['name']

# Label map written to labelmap.pbtxt
with open('./labelmap.pbtxt', 'w') as f:
    f.write(text_format.MessageToString(labelmap))

label_map = label_map_util.load_labelmap('labelmap.pbtxt')
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NCLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# reconstruct frozen graph
def reconstruct(pb_path):
    if not os.path.isfile(pb_path):
        print("Error: %s not found" % pb_path)

    print("Reconstructing Tensorflow model")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(pb_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    print("Success!")
    return detection_graph

detection_graph = reconstruct("ssd_mobilenet_v2_taco_2018_03_29.pb")

# Live streaming for inferencing the model
while cap.isOpened():
    ret, frame = cap.read()
    start = time.time()

    # Converting the frames to tensors
    image_np = np.array(frame)
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

    with detection_graph.as_default():
        gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.01)
        with tf.compat.v1.Session(graph=detection_graph, 
                                    config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)) as sess:
            
            Image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            (boxes, scores, classes, num) = sess.run(
                                                    [detection_boxes, detection_scores,
                                                     detection_classes, num_detections],
                                                     feed_detector = {Image_tensor: input_tensor}
            )
    
            vis_util.visualize_boxes_and_labels_on_image_array(image_np,
                                                                np.squeeze(boxes),
                                                                np.squeeze(classes).astype(np.int32),
                                                                np.squeeze(scores),
                                                                category_index,
                                                                use_normalized_coordinates=True,
                                                                line_thickness=15
            )
            end = time.time()
            total_time = end - start
            fps = 1/total_time
            cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
            cv2.imshow('Yolo Model', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                            break
cap.release()
cv2.destroyAllWindows()
