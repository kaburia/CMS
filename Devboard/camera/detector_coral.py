import cv2
# import tensorflow as tf
from PIL import Image
import time
import os
import numpy as np

import argparse
import time
from matplotlib import cm

from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red')
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill='red')


model = 'yolov5m-int8_edgetpu.tflite'
labels = read_label_file('/home/kali/Desktop/label.txt')
interpreter = make_interpreter(model)
interpreter.allocate_tensors()


cap = cv2.VideoCapture(cv2.CAP_V4L2)

while True:
    ret, frame = cap.read()
    # print('frame' ,frame)
    img = Image.fromarray(frame)
    # print(img)
    # print(img==frame)
    start_time = time.time()
    _, scale = common.set_resized_input(
      interpreter, img.size, lambda size: img.resize(size, Image.ANTIALIAS))
    
    print('----INFERENCE TIME----')
    print('Note: The first inference is slow because it includes',
            'loading the model into Edge TPU memory.')
    
    for _ in range(3):
        start = time.perf_counter()
        interpreter.invoke()
        inference_time = time.perf_counter() - start
        objs = detect.get_objects(interpreter, 0.7, scale)
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
    end_time = time.time()
    total_time = end_time - start_time
    fps = 1/total_time
    
    image = img.convert('RGB')
    draw_objects(ImageDraw.Draw(image), objs, labels)


    cv2.putText(np.array(image), f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
    # Show to screen
    cv2.imshow('OpenCV Feed', np.array(image))
    # image.show()

    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
