FROM cgr.dev/chainguard/python:latest-dev as dev

USER root

WORKDIR /app

RUN pip install pyyaml==6.0.2 
RUN pip install git+https://github.com/openai/whisper.git
RUN pip install numpy
RUN pip install SpeechRecognition
RUN pip install torch
RUN pip install pydub
RUN pip install httpx
RUN pip install --upgrade attrs

RUN pip install python-dateutil
RUN pip install pydub
RUN pip install transformers
RUN pip install openai 
RUN pip install geopy
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt


RUN apk add ffmpeg
RUN apk add curl

RUN pip install openapi-python-client