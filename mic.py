from pathlib import Path
import tkinter as tk
import threading
import pyaudio
import pyttsx3
import wave
import os
import speech_recognition as sr
from googletrans import Translator

engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
translator = Translator()

stop_recording_event = threading.Event()
recording = False
audio_stream = None

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def toggle_recording(recording):
    global stop_recording_event, audio_stream
    if not recording:
        recording = True
        print('recording started...')
        stop_recording_event.clear()
        audio_stream = threading.Thread(target=record_audio)
        audio_stream.start()
    else:
        recording = False
        print('recording stopped...')
        stop_recording_event.set()
    return recording

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
    process_audio(FILE_NAME)

def save_audio(frames, file_name):
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

def process_audio(file_name):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_name) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            ex = translator.detect(text)
            translated_text = translator.translate(text, dest=ex.lang) # type: ignore
            entry.delete("1.0", tk.END)
            entry.insert("1.0", translated_text.text) # type: ignore
            print("Recognized Text:", translated_text.text) # type: ignore
            engine.say(f"Recognized Text was:{translated_text.text}") # type: ignore
            engine.runAndWait()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        engine.say('Could not understand audio...!')
        engine.runAndWait()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        engine.say('Could not recognize audio...!')
        engine.runAndWait()
    finally:
        os.remove(file_name)

def toggle_mic(button, default_image, alternate_image):
    global recording, audio_stream
    current_image = button.cget("image")
    if current_image == str(default_image):
        button.configure(image=alternate_image)        
    else:
        button.configure(image=default_image)
    recording = toggle_recording(recording)

def onMic():
    text = 'hello'
    window = tk.Toplevel()

    window.geometry("250x379")
    window.configure(bg = "#E1E3E9")

    canvas = tk.Canvas(
        window,
        bg = "#E1E3E9",
        height = 379,
        width = 250,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    entry_img = tk.PhotoImage(file=relative_to_assets("entry.png"))
    entry_bg = canvas.create_image(
        124.5,
        120.0,
        image=entry_img
    )
    global entry
    entry = tk.Text(
        window,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry.place(
        x=57.0,
        y=47.0,
        width=135.0,
        height=150.0
    )
    entry.insert("1.0", text)

    clear_img = tk.PhotoImage(file=relative_to_assets("clear.png"))
    clear_btn = tk.Button(
        window,
        image=clear_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: entry.delete("1.0", tk.END),
        relief="flat"
    )
    clear_btn.place(
        x=37.0,
        y=307.0,
        width=180.0,
        height=40.0
    )

    mute_image = tk.PhotoImage(file=relative_to_assets("mute.png"))
    unmute_image = tk.PhotoImage(file=relative_to_assets("unmute.png"))
    mic = tk.Button(
        window,
        image=mute_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_mic(mic, mute_image, unmute_image),
        relief="flat"
    )
    mic.place(
        x=124.0,
        y=219.0,
        width=80.0,
        height=80.0
    )

    mic_img = tk.PhotoImage(
        file=relative_to_assets("mic.png"))
    mic_txt = canvas.create_image(
        88.0,
        259.0,
        image=mic_img
    )
    window.resizable(False, False)
    window.mainloop()
