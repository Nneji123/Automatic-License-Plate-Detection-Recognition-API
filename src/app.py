import io
import os
import sys

import cv2
import numpy as np
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from detections import get_plates_from_image, get_text_from_image

sys.path.append(os.path.abspath(os.path.join("..", "config")))


app = FastAPI(
    title="ANPR(Automatic Number/License Plate Recognition) API",
    description="""An API for recognising vehicle number plates in images and video.""",
    docs_url=None,
    redoc_url=None
)

templates = Jinja2Templates(directory="templates")

favicon_path = "./images/favicon.ico"


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("ocr.html", {"request": request})


@app.post("/ocr_parser")
async def get_ocr(request: Request, file: UploadFile = File(...)):
    # write a function to save the uploaded file and return the file name
    if request.method == "POST":
        form = await request.form()
        if form["file"]:

            files = form["file"]
            contents = io.BytesIO(await files.read())
            file_bytes = np.asarray(bytearray(contents.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cv2.imwrite("./images/image.jpg", img)
            try:
                image = Image.open('./images/image.jpg')
                image = np.array(image)
                img = get_plates_from_image(image)
                text= get_text_from_image(image)
                images = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                images = cv2.resize(images,(800,600), interpolation = cv2.INTER_AREA)
                cv2.imwrite("./images/gen.jpg",images)
                return templates.TemplateResponse(
                    "ocr.html", {"request": request, "sumary": text}
                )
            except ValueError:
                vals = "Error! Please upload a valid image type."
                return vals


@app.get('/gen.png')
async def favicon():
    file_name = "./images/gen.jpg"
    return FileResponse(path=file_name)

@app.get('/img.jpg')
async def background():
    file_name = "./images/img.jpg"
    return FileResponse(path=file_name)

@app.get("/mygif.gif")
async def video_endpoint():
    file_name = "mygif.gif"
    return FileResponse(path=file_name)