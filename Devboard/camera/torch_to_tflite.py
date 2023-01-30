import torch
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf

model = torch.hub.load("ultralytics/yolov5", 'custom', path="best.pt")

img_size = (640, 640)
batch_size = 4
onnx_model_path = 'model.onnx'


model.eval()

sample_input = torch.rand((batch_size, 3, *img_size))

y = model(sample_input)

torch.onnx.export(
    model,
    sample_input, 
    onnx_model_path,
    verbose=False,
    input_names=['input'],
    output_names=['output'],
    opset_version=12
)

# Load the ONNX model
model = onnx.load("model.onnx")

# Check that the model is well formed
onnx.checker.check_model(model)

onnx_model_path = 'model.onnx'
tf_model_path = 'model_tf'

onnx_model = onnx.load(onnx_model_path)
tf_rep = prepare(onnx_model)
tf_rep.export_graph(tf_model_path)

saved_model_dir = 'model_tf'
tflite_model_path = 'model.tflite'

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
tflite_model = converter.convert()

# Save the model
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)