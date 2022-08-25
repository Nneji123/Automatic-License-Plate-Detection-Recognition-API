import fileinput
import os
from pathlib import Path
from typing import Union
from paddleocr import PaddleOCR
import torch
import cv2
import numpy as np
import re
from deep_sort_realtime.deepsort_tracker import DeepSort


def prepend_text(filename: Union[str, Path], text: str):
    with fileinput.input(filename, inplace=True) as file:
        for line in file:
            if file.isfirstline():
                print(text)
            print(line, end="")

# if not os.path.isdir('yolov7'):
#     yolov7_repo_url = 'https://github.com/WongKinYiu/yolov7'
#     os.system(f'git clone {yolov7_repo_url}')
#     # Fix import errors
#     for file in ['yolov7/models/common.py', 'yolov7/models/experimental.py', 'yolov7/models/yolo.py', 'yolov7/utils/datasets.py']:
#          prepend_text(file, "import sys\nsys.path.insert(0, './yolov7')")

from models.experimental import attempt_load
from utils.general import check_img_size
from utils.torch_utils import select_device, TracedModel
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box

weights = 'weights.pt'
device_id = 'cpu'
image_size = 640
trace = True

# # Initialize
device = select_device(device_id)
half = device.type != 'cpu'  # half precision only supported on CUDA

# # Load model
model = attempt_load(weights, map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride
imgsz = check_img_size(image_size, s=stride)  # check img_size

# if trace:
#     model = TracedModel(model, device, image_size)

# if half:
#     model.half()  # to FP16
    
# if device.type != 'cpu':
#     model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

model.eval()

# Load OCR

paddle = PaddleOCR(lang="en")

def detect_plate(source_image):
    # Padded resize
    img_size = 640
    stride = 32
    img = letterbox(source_image, img_size, stride=stride)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
        
    with torch.no_grad():
        # Inference
        pred = model(img, augment=True)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.25, 0.45, classes=0, agnostic=True)

    plate_detections = []
    det_confidences = []
    
    # Process detections
    for i, det in enumerate(pred):  # detections per image
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], source_image.shape).round()

            # Return results
            for *xyxy, conf, cls in reversed(det):
                coords = [int(position) for position in (torch.tensor(xyxy).view(1, 4)).tolist()[0]]
                plate_detections.append(coords)
                det_confidences.append(conf.item())

    return plate_detections, det_confidences


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=2.0, threshold=0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def crop(image, coord):
    cropped_image = image[int(coord[1]):int(coord[3]), int(coord[0]):int(coord[2])]
    return cropped_image

def ocr_plate(plate_region):
    # Image pre-processing for more accurate OCR
    rescaled = cv2.resize(plate_region, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    grayscale = cv2.cvtColor(rescaled, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    dilated = cv2.dilate(grayscale, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    sharpened = unsharp_mask(eroded)

    # OCR the preprocessed image
    results = paddle.ocr(sharpened, det=False, cls=False)
    maxConfidenceResult = max(results, key=lambda result:result[1])
    plate_text, ocr_confidence = maxConfidenceResult

    # Filter out anything but uppercase letters, digits, hypens and whitespace.
    plate_text = re.sub(r'[^-A-Z0-9 ]', r'', plate_text).strip()
    
    if ocr_confidence == 'nan':
        ocr_confidence = 0
    
    return plate_text, ocr_confidence
    
from copy import deepcopy

def get_plates_from_image(input):
    if input is None:
        return None
    plate_detections, det_confidences = detect_plate(input)
    plate_texts = []
    ocr_confidences = []
    detected_image = deepcopy(input)
    for coords in plate_detections:
        plate_region = crop(input, coords)
        plate_text, ocr_confidence = ocr_plate(plate_region)
        plate_texts.append(plate_text)
        ocr_confidences.append(ocr_confidence)
        plot_one_box(coords, detected_image, label=plate_text, color=[0, 150, 255], line_thickness=2)
    return detected_image

def get_text_from_image(input):
    if input is None:
        return None
    plate_detections, det_confidences = detect_plate(input)
    plate_texts = []
    ocr_confidences = []
    detected_image = deepcopy(input)
    for coords in plate_detections:
        plate_region = crop(input, coords)
        plate_text, ocr_confidence = ocr_plate(plate_region)
        plate_texts.append(plate_text)
        ocr_confidences.append(ocr_confidence)
        plot_one_box(coords, detected_image, label=plate_text, color=[0, 150, 255], line_thickness=2)
    return plate_text

def pascal_voc_to_coco(x1y1x2y2):
    x1, y1, x2, y2 = x1y1x2y2
    return [x1, y1, x2 - x1, y2 - y1]

def get_best_ocr(preds, rec_conf, ocr_res, track_id):
    for info in preds:
    # Check if it is current track id
        if info['track_id'] == track_id:
          # Check if the ocr confidenence is maximum or not
            if info['ocr_conf'] < rec_conf:
                info['ocr_conf'] = rec_conf
                info['ocr_txt'] = ocr_res
            else:
                rec_conf = info['ocr_conf']
                ocr_res = info['ocr_txt']
            break
    return preds, rec_conf, ocr_res

def get_plates_from_video(source):
    if source is None:
        return None
    
    # Create a VideoCapture object
    video = cv2.VideoCapture(source)

    # Default resolutions of the frame are obtained. The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object.
    temp = f'{Path(source).stem}_temp{Path(source).suffix}'
    export = cv2.VideoWriter(temp, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    # Intializing tracker
    tracker = DeepSort(embedder_gpu=False)
    
    # Initializing some helper variables.
    preds = []
    total_obj = 0

    while(True):
        ret, frame = video.read()
        if ret == True:
            # Run the ANPR algorithm
            bboxes, scores = detect_plate(frame)
            # Convert Pascal VOC detections to COCO
            bboxes = list(map(lambda bbox: pascal_voc_to_coco(bbox), bboxes))
            
            if len(bboxes) > 0:
                # Storing all the required info in a list.
                detections = [(bbox, score, 'number_plate') for bbox, score in zip(bboxes, scores)]

                # Applying tracker.
                # The tracker code flow: kalman filter -> target association(using hungarian algorithm) and appearance descriptor.
                tracks = tracker.update_tracks(detections, frame=frame)

                # Checking if tracks exist.
                for track in tracks:
                    if not track.is_confirmed() or track.time_since_update > 1:
                        continue

                    # Changing track bbox to top left, bottom right coordinates
                    bbox = [int(position) for position in list(track.to_tlbr())]
                    
                    for i in range(len(bbox)):
                        if bbox[i] < 0:
                            bbox[i] = 0

                    # Cropping the license plate and applying the OCR.
                    plate_region = crop(frame, bbox)
                    plate_text, ocr_confidence = ocr_plate(plate_region)

                    # Storing the ocr output for corresponding track id.
                    output_frame = {'track_id': track.track_id, 'ocr_txt': plate_text, 'ocr_conf': ocr_confidence}

                    # Appending track_id to list only if it does not exist in the list
                    # else looking for the current track in the list and updating the highest confidence of it.
                    if track.track_id not in list(set(pred['track_id'] for pred in preds)):
                        total_obj += 1
                        preds.append(output_frame)
                    else:
                        preds, ocr_confidence, plate_text = get_best_ocr(preds, ocr_confidence, plate_text, track.track_id)
                    
                    # Plotting the prediction.
                    plot_one_box(bbox, frame, label=f'{str(track.track_id)}. {plate_text}', color=[255, 150, 0], line_thickness=3)
            
            # Write the frame into the output file
            export.write(frame)
        else:
            break 

    # When everything done, release the video capture and video write objects
    
    video.release()
    export.release()

    #Compressing the output video for smaller size and web compatibility.
    output = f'{Path(source).stem}_detected{Path(source).suffix}'
    # os.system(f'ffmpeg -y -i {temp} -c:v libx264 -b:v 5000k -minrate 1000k -maxrate 8000k -pass 1 -c:a aac -f mp4 /dev/null && ffmpeg -i {temp} -c:v libx264 -b:v 5000k -minrate 1000k -maxrate 8000k -pass 2 -c:a aac -movflags faststart {output}')
    # os.system(f'rm -rf {temp} ffmpeg2pass-0.log ffmpeg2pass-0.log.mbtree')

    return output