import os
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse, FileResponse
import numpy as np
import io
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
import pytesseract
from .helpers import get_plate, load_model, preprocess_image
import onnxruntime 


app = FastAPI()



@app.get('/')
def home():
    return {'Title': 'Super Resolution and Colorisation API'}


# endpoint for just enhancing the image
@app.post("/predict")
async def predict_plot_image(file: UploadFile = File(...)):
    

    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 
    #res, im_png = cv2.imencode(".png", im_rgb)
    cv2.imwrite("image.jpg", img)
    vehicle, LpImg, cor = get_plate("image.jpg")
    fig = plt.figure(figsize=(12,6))
    grid = gridspec.GridSpec(ncols=2,nrows=1,figure=fig)
    print(vehicle.shape)
    fig.add_subplot(grid[1])
    plt.axis(False)
    plt.imshow(LpImg[0])
    plt.savefig("newimage.jpg")
    #cv2.imwrite("newimage.jpg", LpImg[0])
    return FileResponse("newimage.jpg", media_type="image/jpg")

@app.post('/detect')
async def get_ocr(file: UploadFile = File(...)) -> str:
    
    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 
    #res, im_png = cv2.imencode(".png", im_rgb)
    cv2.imwrite("image.jpg", img)
    vehicle, LpImg, cor = get_plate("image.jpg")
    fig = plt.figure(figsize=(12,6))
    grid = gridspec.GridSpec(ncols=2,nrows=1,figure=fig)
    print(vehicle.shape)
    fig.add_subplot(grid[1])
    plt.axis(False)
    plt.imshow(LpImg[0])
    plt.savefig("newimage.jpg")
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
    return new_string

