import contextlib
import wave
import os
from glimpse_api_client.glimpse_api_client import Client, models
from glimpse_api_client.glimpse_api_client.api.default import post_transcriptions
import datetime
class TranscribedChunk():
    def __init__(self, audio_chunk, transcription_text, time):
        self.audio_chunk = audio_chunk
        self.text = transcription_text
        self.time = time

class AudioChunk():
    def __init__(self, audio, sample_rate):
        """
        args:
            audio: a wave audio bytestream
            sample_rate: sample rate of the wave audio
        """
        self.audio = audio
        self.sample_rate = sample_rate

def write_text(path, text):
    """Writes a transcription chunk.

    Takes path and text and writes the text to the path
    """
    with open(path, 'w') as txtfile:
        txtfile.write(text)

def write_wave(path, audio, sample_rate):
    """Writes a .wav file.

    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

class Writer():
    def __init__(self, name, base_path):
        self.name = name
        self.base_path = base_path

    def handle_transcription(self, transcribed_chunk):
        dest_path = os.path.join(self.base_path, self.name, transcribed_chunk.time.isoformat())
        os.makedirs(dest_path)
        text_file_path = os.path.join(dest_path, "transcription.txt")
        audio_file_path = os.path.join(dest_path, "audio.wav")
        write_text(text_file_path, transcribed_chunk.text)
        write_wave(audio_file_path, transcribed_chunk.audio_chunk.audio, transcribed_chunk.audio_chunk.sample_rate)
    
class APIWriter(Writer):
    def __init__(self, name, base_path):
        super().__init__(name, base_path)

    def handle_transcription(self, transcribed_chunk):

        if len(transcribed_chunk.text.split()) < 3:
            # If there are less than 3 words in a message assume it's garbage
            return


        dest_path = os.path.join(self.base_path, self.name, transcribed_chunk.time.isoformat())
        os.makedirs(dest_path)
        audio_file_path = os.path.join(dest_path, "audio.wav")
        write_wave(audio_file_path, transcribed_chunk.audio_chunk.audio, transcribed_chunk.audio_chunk.sample_rate)

        transcription = models.Transcription(content=transcribed_chunk.text, audio=audio_file_path, timestamp=datetime.datetime.now(datetime.UTC))
        
        client = Client(base_url=os.environ["API_URL"])
        response = post_transcriptions.sync_detailed(
            client=client,
            body=transcription
        )

        print(f"RESPONSE: {response}")
