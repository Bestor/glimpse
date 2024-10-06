FROM cgr.dev/chainguard/python:latest-dev as dev

USER root

WORKDIR /app

#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
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


RUN apk add ffmpeg
RUN apk add curl