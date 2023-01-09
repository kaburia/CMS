# Converting trained model to tflite and using the script for inference on edge
import tflite_runtime.interpreter as tflite

# class TestModel(tf.Module):
#       def __init__(self):
#         super(TestModel, self).__init__()

#       @tf.function(input_signature=[tflite.TensorSpec(shape=[1, 10], dtype=tflite.float32)])
#       def add(self, x):
#         '''
#         Simple method that accepts single input 'x' and returns 'x' + 4.
#         '''
#         # Name the output 'result' for convenience.
#         return {'result' : x + 4}


# SAVED_MODEL_PATH = 'content/saved_models/test_variable'
TFLITE_FILE_PATH = 'action3.tflite'

# # Save the model
# module = TestModel()
# # You can omit the signatures argument and a default signature name will be
# # created with name 'serving_default'.
# tflite.saved_model.save(
#     module, SAVED_MODEL_PATH,
#     signatures={'my_signature':module.add.get_concrete_function()})

# # Convert the model using TFLiteConverter
# converter = tflite.TFLiteConverter.from_saved_model(SAVED_MODEL_PATH)
# tflite_model = converter.convert()
# with open(TFLITE_FILE_PATH, 'wb') as f:
#   f.write(tflite_model)

# Load the TFLite model in TFLite Interpreter
interpreter = tflite.Interpreter(TFLITE_FILE_PATH)
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(output_details)
print()
print(input_details)

# There is only 1 signature defined in the model,
# so it will return it by default.
# If there are multiple signatures then we can pass the name.
# my_signature = interpreter.get_signature_runner()

# # my_signature is callable with input as arguments.
# output = my_signature(x=tflite.constant([1.0], shape=(1,10), dtype=tflite.float32))
# # 'output' is dictionary with all outputs from the inference.
# # In this case we have single output 'result'.
# print(output['result']) 
