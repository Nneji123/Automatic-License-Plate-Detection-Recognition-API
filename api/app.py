import io
import os
import sys

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from PIL import Image
from detections import get_plates_from_image, get_text_from_image

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
    cv2.imwrite("image.jpg", img)
    try:
        image = Image.open('image.jpg')
        image = np.array(image)
        img = get_plates_from_image(image)
        images = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        print("Detecting plates from image...")
        cv2.imwrite("output.jpg", images)
        return FileResponse("output.jpg", media_type="image/jpg")
    except ValueError:
        vals = "Error! Please upload a valid image type."
        return vals

@app.post("/detect-plate-text")
async def detect_plate_text(file: UploadFile = File(...)):

    contents = io.BytesIO(await file.read())
    file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    cv2.imwrite("image.jpg", img)
    try:
        image = Image.open('image.jpg')
        image = np.array(image)
        text= get_text_from_image(image)
        return {"License Plate": text}
    except ValueError:
        vals = "Error! Please upload a valid image type."
        return vals