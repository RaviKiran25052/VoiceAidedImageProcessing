import threading
import pyaudio
import wave
import speech_recognition as sr
from googletrans import Translator
from queue import Queue
from display import showText

translator = Translator()
recording = False
stop_recording_event = threading.Event()
audio_stream = None
queue = Queue()

def check_queue():
   while True:
      if not queue.empty():
         translated_text = queue.get()
         showText(translated_text)

def toggle_recording(recording):
   global stop_recording_event, audio_stream

   if not recording:
      recording = True
      stop_recording_event.clear()
      audio_stream = threading.Thread(target=record_audio)
      audio_stream.start()
   else:
      recording = False
      stop_recording_event.set()
      
def record_audio():
   CHUNK = 1024
   FORMAT = pyaudio.paInt16
   CHANNELS = 1
   RATE = 44100
   RECORD_SECONDS = 5
   FILE_NAME = "temp.wav"

   p = pyaudio.PyAudio()

   stream = p.open(
      format=FORMAT,
      channels=CHANNELS,
      rate=RATE,
      input=True,
      frames_per_buffer=CHUNK
   )

   frames = []

   while not stop_recording_event.is_set():
      frames.append(stream.read(CHUNK))

   stream.stop_stream()
   stream.close()
   p.terminate()

   save_audio(frames, FILE_NAME)
   translated_text = speech_to_text()
   
   queue_checker_thread = threading.Thread(target=check_queue)
   queue_checker_thread.start()
   queue.put(translated_text)

def save_audio(frames, file_name):
   with wave.open(file_name, 'wb') as wf:
      wf.setnchannels(1)
      wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
      wf.setframerate(44100)
      wf.writeframes(b''.join(frames))

def speech_to_text():
    recognizer = sr.Recognizer()
    
    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        ex = translator.detect(text)
        translated_text = translator.translate(text, dest=ex.lang) # type: ignore
        return translated_text.text # type: ignore
    except sr.UnknownValueError:
        return "Sorry, could not understand audio."
    except sr.RequestError as e:
        return f"Error occurred: {e}"
