FROM python:3.8

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install torch==1.10.0+cu111 torchvision==0.11.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html --upgrade

COPY . /app
WORKDIR /app    

ENTRYPOINT ["python"]
CMD ["app.py"]