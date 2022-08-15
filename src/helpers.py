import tensorflow as tf
#tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import cv2
import numpy as np
from utils import detect_lp
from tensorflow.keras.models  import model_from_json
from os.path import splitext,basename
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
import glob

def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        print("Model Loaded successfully...")
        print("Detecting License Plate ... ")
        return model
    except Exception as e:
        print(e)
wpod_net_path = "./models/wpod-net.json"
wpod_net = load_model(wpod_net_path)

def preprocess_image(image_path,resize=False):
    img = cv2.imread(image_path)
    from PIL import Image
    #img = Image.open(image_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img

def get_plate(image_path, Dmax=608, Dmin = 608):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    return vehicle, LpImg, cor

# test_image_path = "stock.jpg"
# vehicle, LpImg, cor = get_plate(test_image_path)

# fig = plt.figure(figsize=(12,6))
# #grid = gridspec.GridSpec(ncols=2,nrows=1,figure=fig)
# #fig.add_subplot(grid[0])
# #plt.axis(False)
# #plt.imshow(vehicle)
# grid = gridspec.GridSpec(ncols=2,nrows=1,figure=fig)
# print(vehicle.shape)
# fig.add_subplot(grid[1])
# plt.axis(False)
# plt.imshow(LpImg[0])




