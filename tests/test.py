import os
import sys

sys.path.append(os.path.abspath(os.path.join("..", "config")))

#from fastapi import FastAPI
#from fastapi.testclient import TestClient

from src.helpers import get_text_ocr
import warnings
warnings.filterignore()

def test_ocr():
    assert get_text_ocr("image.jpg") == " CZ20 FSE"


