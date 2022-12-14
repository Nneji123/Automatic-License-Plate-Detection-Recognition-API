import io
import os
import sys

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from PIL import Image
from detections import get_plates_from_image, get_text_from_image, get_plates_from_video

sys.path.append(os.path.abspath(os.path.join("..", "config")))


app = FastAPI(
    title="ANPR(Automatic Number/License Plate Recognition) API",
    description="""An API for recognising vehicle number plates in images and video.""",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=PlainTextResponse, tags=["home"])
async def home():
    note = """
    ANPR(Automatic Number/License Plate Recognition) API"
    An API for recognising vehicle number plates in images and video.
    Note: add "/redoc" to get the complete documentation.
    """
    return note


@app.post("/detect-plate")
async def detect_plate(file: UploadFile = File(...)):

    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    cv2.imwrite("./images/image.jpg", img)
    try:
        image = Image.open('./images/image.jpg')
        image = np.array(image)
        img = get_plates_from_image(image)
        images = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        print("Detecting plates from image...")
        cv2.imwrite("./images/output.jpg", images)
        return FileResponse("input_temp.mp4", media_type="video/mp4")
    except ValueError:
        vals = "Error! Please upload a valid image type."
        return vals

@app.post("/detect-plate-text")
async def detect_plate_text(file: UploadFile = File(...)):

    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    cv2.imwrite("./images/image.jpg", img)
    try:
        image = Image.open('./images/image.jpg')
        image = np.array(image)
        text= get_text_from_image(image)
        return {"License Plate": text}
    except ValueError:
        vals = "Error! Please upload a valid image type."
        return vals

@app.post("/detect-plate-video")
async def detect_plate_video(file: UploadFile = File(...)):

    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    FILE_INPUT = './images/input.mp4'
    if os.path.isfile(FILE_INPUT):
        os.remove(FILE_INPUT)

    with open(FILE_INPUT, "wb") as input_file:  # open for [w]riting as [b]inary
        input_file.write(file_bytes)
    try:
        #cap = cv2.VideoCapture('video.mp4')
        #image = np.array(image)
        #text= get_plates_from_video('input.mp4')
        #cv2.imwrite('vids.mp4', text)
        return FileResponse("input_temp.mp4", media_type="video/mp4")
        # print('File converted')
    except ValueError:
        vals = "Error! Please upload a valid image type."
        return vals
