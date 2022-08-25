import os
if not os.path.isfile('weights.pt'):
    weights_url = 'https://archive.org/download/anpr_weights/weights.pt'
    os.system(f'wget {weights_url}')
    print("Downloaded files!")


from detections import get_plates_from_image
from PIL import Image
import numpy as np
image = Image.open('./images/image.jpg')
image = np.array(image)
img = get_plates_from_image(image)
print("Downloaded and loaded all files!")