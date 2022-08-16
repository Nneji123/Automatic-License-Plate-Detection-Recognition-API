<h1 align="center">Automatic Vehicle Number Plate Recognition</h1>

<p align="center">
  <img width="700" height="300" src="https://user-images.githubusercontent.com/101701760/184875740-365bf49c-03f0-4d85-9001-40608353a212.png">
</p>


[![Language](https://img.shields.io/badge/Python-darkblue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![HTML](https://img.shields.io/badge/HTML-black.svg?style=flat&logo=html5&logoColor=white)](http://avnprapp.herokuapp.com)
[![CSS](https://img.shields.io/badge/CSS-yellow.svg?style=flat&logo=css3&logoColor=white)](http://avnprapp.herokuapp.com)
[![Framework](https://img.shields.io/badge/Keras-darkred.svg?style=flat&logo=keras&logoColor=white)](http://www.Keras.org/news.html)
[![Framework](https://img.shields.io/badge/FastAPI-darkgreen.svg?style=flat&logo=fastapi&logoColor=white)](https://https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API-api.herokuapp.com/docs)
![hosted](https://img.shields.io/badge/Heroku-430098?style=flat&logo=heroku&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)
[![Gitpod](https://img.shields.io/badge/Gitpod-orange?style=flat&logo=gitpod&logoColor=white)](https://gitpod.io/#https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API)
![reposize](https://img.shields.io/github/repo-size/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API.git)


## About
>Automatic Vehicle Number Plate Recognition(AVNPR) Application built with FastAPI, Keras, HTML and CSS. 

HTML Web App: http://avnprapp.herokuapp.com

API Documentation: http://avnprapi.herokuapp.com/docs

Official API Docker Image: https://hub.docker.com/repository/docker/nneji123/avnprapi

## Table of Contents
  * [About](#about)
  * [Table of Contents](#table-of-contents)
    + [Features](#features)
  * [Repository File Structure](#repository-file-structure)
  * [Demo](#demo)
    + [API Demo](#api-demo)
    + [HTML App Demo](#html-app-demo)
    + [Streamlit App Demo](#streamlit-app-demo)
  * [How to run the Application](#how-to-run-the-application)
  * [Tests](#tests)
  * [Deployment](#deployment)
- [Todo](#todo)
- [License](#license)



## Repository File Structure
```bash
├── api
│   ├── app.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── helpers.py
│   ├── heroku.yml
│   ├── images
│   ├── __init__.py
│   ├── models
│   ├── requirements.txt
│   ├── save_model.py
│   └── utils.py
├── LICENSE
├── README.md
├── sample_images
├── src
│   ├── app.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── helpers.py
│   ├── images
│   ├── __init__.py
│   ├── models
│   ├── requirements.txt
│   ├── save_model.py
│   ├── templates
│   │   └── ocr.html
│   └── utils.py
└── tests
```

## Features
This application uses machine learning algorithms to detect and recognise number plate or license plates of cars in an image.

## Demo
### API Demo
### HTML App Demo

## How to run the Application
<details> 
  <summary><b>Running on Local Machine</b></summary>

**To run the application on your local system do the following:**
1. Clone the repository:
```bash
git clone https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API.git
```

2. Change the directory:
```
cd https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API
```

3. Install the requirements:
```
pip install -r requirements.txt
```

4. Run the application
```
uvicorn app:app --reload --port 8000
```
**You should be able to view the application by going to http://127.0.0.1:8000/**
</details>

<details> 
  <summary><b>Running on Local Machine with Docker Compose</b></summary>

**You can also run the application in a docker container using docker compose(if you have it installed)**

1. Clone the repository:
```bash
git clone https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API.git
```

2. Change the directory:
```
cd https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API
```

3. Run the docker compose command
```docker
docker compose up -d --build 
```
You should be able to view the application by going to http://localhost:8000/
</details>


<details> 
  <summary><b>Running in a Gitpod Cloud Environment</b></summary>


**Click the button below to start a new development environment:**

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API)
</details>

## Tests
<details> 
  <summary><b>Test HTML Web App Functions</b></summary>

To test the HTML Web app do the following:
1. Clone the repository:
```
git clone https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API.git
```
2. Change the working directory and install the requirements and pytest:
```
cd src && pip install -r requirements.txt && pip install pytest
```
3. Move to the tests folder and run the tests
```
cd .. && cd tests && pytest
```
</details>

<details> 
  <summary><b>Test API</b></summary>

To test the API functions do the following:
1. Clone the repository:
```
git clone https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API.git
```
2. Change the working directory and install the requirements and pytest:
```
cd api && pip install -r requirements.txt && pip install pytest
```
3. Move to the tests folder and run the tests
```
cd .. && cd tests && pytest
```
</details>

## Deployment

<details> 
  <summary><b>Deploying the Application to Heroku</b></summary>

**Assuming you have git and heroku cli installed just carry out the following steps:**

1. Clone the repository:
```bash
git clone https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API.git
```

2. Change the directory:
```
cd https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API
```

3. Login to Heroku

``` 
heroku login
heroku container:login
```

4. Create your application
```
heroku create your-app-name
```
Replace **your-app-name** with the name of your choosing.

5. Build the image and push to Container Registry:

```
heroku container:push web
```

6. Then release the image to your app:
 
```
heroku container:release web
```

Click the button below to deploy the application.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)



</details>

<details> 
  <summary><b>How to deploy the application on AWS EC2 using a Bash Script</b></summary>

**1. Fork this repository**

**2. Login to AWS, create a new AWS EC2 instance and make sure to allow outside traffic as shown in the screenshots below:**

<img src="https://user-images.githubusercontent.com/101701760/178163392-3c9fc8ec-e58a-420d-a6bb-2885215d8105.png" width="1200" height="400">


<img src="https://user-images.githubusercontent.com/101701760/178163373-e4bb2c92-0f47-4a22-9556-dfc470fd7e8a.png" width="1200" height="400">


**3. When the instance has been launched, copy the Public IP address of your instance and paste it in the 'fastapi_setup' file of your cloned repository as shown below**

<img src="https://user-images.githubusercontent.com/101701760/178163457-2e156379-b542-4d24-aebf-e202dd44ae2c.png" width="1200" height="400">

<img src="https://user-images.githubusercontent.com/101701760/178163536-918818ee-563d-4b0d-a5ec-5c265a75b2b4.png" width="1200" height="400">


**4. Connect to your instance and clone your forked repository, an example in my case:**
```bash
git clone https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API.git
```
**5. cd into your repository which is probably named 'https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API'. You can do that by running:**
```bash
cd https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API 
```
**6. Then run the setup.sh file to get your application up and running:**
```bash
chmod u+x aws.sh
./aws.sh
```
**You can then view the application by going to your Public IP's location, an example in my case will be:
http://3.95.202.74:80/docs**

**You can also watch this video for a more in depth explanation on how to deploy a FastAPI application on AWS EC2:**
[![How to deploy FastAPI on AWS](https://youtube-md.vercel.app/SgSnz7kW-Ko/640/360)](https://www.youtube.com/watch?v=SgSnz7kW-Ko)
</details>

<details> 
  <summary><b>Deploying the Application with AWS Lightsail</b></summary>

To deploy the application using aws Lightsail just watch the video below and follow the steps.

</details>

<details>
    <summary><b>Deploy the Application to Railway<b></summary>
Click the button below to deploy the Application to railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/k_WXDI?referralCode=ZYOf2M)

</details>



## License
[MIT](https://github.com/Nneji123/https://github.com/Nneji123/Automatic-License-Plate-Detection-Recognition-API/LICENSE)


## TODO
- [ ] add tests
- [x] update documentation
- [x] deployment
- [ ] github actions
- [ ] update api
- [ ] update app
