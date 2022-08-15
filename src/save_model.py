# simple script to convert rdn model to onnx
import os 
from tensorflow import keras
model = keras.models.load_model('model.h5')
model.save('my_model')
os.system("python -m tf2onnx.convert --saved-model my_model --output model.onnx --opset 13")