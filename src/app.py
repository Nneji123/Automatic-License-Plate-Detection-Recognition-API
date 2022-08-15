import os
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse, FileResponse
import numpy as np
import io
from PIL import Image
import cv2
import warnings
from .helpers import get_plate, load_model, preprocess_image
import onnxruntime 


app = FastAPI()



@app.get('/')
def home():
    return {'Title': 'Super Resolution and Colorisation API'}


# endpoint for just enhancing the image
@app.post("/enhance")
async def root(file: UploadFile = File(...)):
    

    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 
    #res, im_png = cv2.imencode(".png", im_rgb)
    cv2.imwrite("image.jpg", img)
    vehicle, LpImg, cor = get_plate("image.jpg")
    im_rgb = cv2.cvtColor(pred[:, :, 0], cv2.COLOR_BGR2RGB)
    res, im_png = cv2.imencode(".png", im_rgb)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

