#! python3.7

import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
import requests
import io
import datetime
from queue import Queue
from pydub import AudioSegment
import time
from sys import platform
import threading
import ssl
import contextlib
import wave
from core.writer import AudioChunk, TranscribedChunk
ssl._create_default_https_context = ssl._create_unverified_context

class BroadcastifyFeed():
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password



def stream_to_bytes(feed, data_queue, recorder, chunk_size=1024, save_interval=10):
    auth = requests.auth.HTTPBasicAuth(feed.user, feed.password)
    response = requests.get(feed.url, stream=True, auth=auth)
    response.raise_for_status()

    byte_stream = io.BytesIO()

    start_time = time.time()

    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            byte_stream.write(chunk)

            if time.time() - start_time >= save_interval:
                # Take the raw byte stream and convert it to an mp3 audio segment
                byte_stream.seek(0)
                audio = AudioSegment.from_file(byte_stream, format="mp3")

                # Convert the mp3 bytestream into a .wav stream. Whsiper needs .wav
                wav_buffer = io.BytesIO()
                audio.export(wav_buffer, format="wav")
                wav_buffer.seek(0)
                source = sr.AudioFile(wav_buffer)

                # Tune the recorder to ignore ambient noise in the audio chunk
                with source:
                    recorder.adjust_for_ambient_noise(source)

                # Put the wav bytes on the queue for processing by whisper
                data_queue.put(wav_buffer.read())

                start_time = time.time()
                byte_stream = io.BytesIO()  # Reset the byte stream for the next interval

def process(feed, audio_model, writer, energy_threshold=1000, phrase_timeout=3):
    """
    args:
        feed_url: BroadcastifyFeed object 
        audio_model: an instantiated whsiper model
        energy_threshold: Energy level required for recording to start
        phrase_timeout: How much empty space exists in the stream before it gets counted as a new transcription 
    """
    # The last time a recording was retrieved from the queue.
    phrase_time = None
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = energy_threshold 
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    # Create a background thread that pushes chunks of the audio stream onto a queue to be processed
    listener_thread = threading.Thread(target=stream_to_bytes, args=(feed, data_queue, recorder))
    listener_thread.daemon = True
    listener_thread.start()

    while True:
        now = datetime.datetime.now(datetime.UTC)
        # Pull raw recorded audio from the queue.
        if not data_queue.empty():
            phrase_complete = False
            # If enough time has passed between recordings, consider the phrase complete.
            # Clear the current working audio buffer to start over with the new data.
            if phrase_time and now - phrase_time > datetime.timedelta(seconds=phrase_timeout):
                phrase_complete = True
            # This is the last time we received new audio data from the queue.
            phrase_time = now
            
            # Combine audio data from queue
            audio_data = b''.join(data_queue.queue)
            data_queue.queue.clear()
            
            # Convert in-ram buffer to something the model can use directly without needing a temp file.
            # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
            # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            # Read the transcription.
            result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
            text = result['text'].strip()

            # If we detected a pause between recordings, add a new item to our transcription.
            # Otherwise edit the existing one.
            if phrase_complete:
                audio_chunk = AudioChunk(audio=audio_data, sample_rate=16000)
                transcribed_chunk = TranscribedChunk(audio_chunk=audio_chunk, transcription_text=text, time=phrase_time)
                writer.handle_transcription(transcribed_chunk)

        else:
            # Infinite loops are bad for processors, must sleep.
            time.sleep(0.25)

