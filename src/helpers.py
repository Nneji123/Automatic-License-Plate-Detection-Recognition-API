import tensorflow as tf
import cv2
import numpy as np
from utils import detect_lp
from tensorflow.keras.models  import model_from_json
from os.path import splitext,basename
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
import pytesseract
import glob
from PIL import Image

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

def get_text_ocr(image_path:str) -> str:
    vehicle, LpImg, cor = get_plate(image_path)
    value = np.array(LpImg[0], dtype=np.float32)
    pred_img = Image.fromarray((value * 255).astype(np.uint8)).convert('RGB')
    pred_img.save('newimage.jpg')
    #cv2.imwrite("newimage.jpg", LpImg[0])
    image = Image.open("newimage.jpg")
    # Extracting text from image
    custom_config = r"-l eng --oem 3 --psm 6"
    text = pytesseract.image_to_string(image, config=custom_config)

    # Remove symbol if any
    characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
    new_string = text
    for character in characters_to_remove:
        new_string = new_string.replace(character, "")

    # Converting string into list to dislay extracted text in seperate line
    new_string = new_string.split("\n")
    return new_string[0]

