import os
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse, FileResponse
import numpy as np
import io
from PIL import Image
import cv2
import warnings
import onnxruntime 


app = FastAPI()



@app.get('/')
def home():
    return {'Title': 'Super Resolution and Colorisation API'}


# endpoint for just enhancing the image
@app.post("/enhance")
async def root(file: UploadFile = File(...)):
    

    contents = io.BytesIO(await file.read())
    new_img = Image.open(contents) 
    x = np.array(new_img,dtype=np.float32) 
    x = np.expand_dims(x, axis=0)
    sess = onnxruntime.InferenceSession("./src/models/model.onnx")
    x = x if isinstance(x, list) else [x]
    feed = dict([(input.name, x[n]) for n, input in enumerate(sess.get_inputs())])
    pred_onnx = sess.run(None,  feed)[0]
    pred = np.squeeze(pred_onnx)
    im_rgb = cv2.cvtColor(pred[:, :, 0], cv2.COLOR_BGR2RGB)
    res, im_png = cv2.imencode(".png", im_rgb)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

