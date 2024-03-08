import os
import pyttsx3
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from mic import onMic
from capture import oncamera

engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

recording = False

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def listenAudio():
    file_path = 'audio.mp3'
    if os.path.exists(file_path):
        os.system("start audio.mp3")
    else:
        engine.say('No audio saved..!')
        engine.runAndWait()

def onOff(button, default_image, alternate_image):
    current_image = button.cget("image")
    if current_image == str(default_image):
        button.configure(image=alternate_image)
        capture['state'] = "normal"
        speak['state'] = "normal"
        listen['state'] = "normal"
    else:
        button.configure(image=default_image)
        capture['state'] = "disabled"
        speak['state'] = "disabled"
        listen['state'] = "disabled"

window = Tk()
window.geometry("250x333")
window.configure(bg = "#E1E3E9")

canvas = Canvas(
    window,
    bg = "#E1E3E9",
    height = 333,
    width = 250,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
cap_image = PhotoImage(file=relative_to_assets("capture.png"))
capture = Button(
    window,
    image=cap_image,
    borderwidth=0,
    highlightthickness=0,
    state="disabled",
    command=lambda: oncamera(),
    relief="flat"
)
capture.place(
    x=24.0,
    y=247.0,
    width=200.0,
    height=50.0
)

listen_image = PhotoImage(file=relative_to_assets("listen.png"))
listen = Button(
    image=listen_image,
    borderwidth=0,
    highlightthickness=0,
    state="disabled",
    command=lambda: listenAudio(),
    relief="flat"
)
listen.place(
    x=24.0,
    y=95.0,
    width=200.0,
    height=50.0
)

speak_img = PhotoImage(file=relative_to_assets("speak.png"))
speak = Button(
    image=speak_img,
    borderwidth=0,
    highlightthickness=0,
    state="disabled",
    command=lambda: onMic(),
    relief="flat"
)
speak.place(
    x=25.0,
    y=171.0,
    width=200.0,
    height=50.0
)

off_text = PhotoImage(file=relative_to_assets("off.png"))
offText = canvas.create_image(
    192.0,
    50.0,
    image=off_text
)

toggle_off = PhotoImage(file=relative_to_assets("toggle_off.png"))
toggle_on = PhotoImage(file=relative_to_assets("toggle_on.png"))
toggle = Button(
    image=toggle_off,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: onOff(toggle, toggle_off, toggle_on),
    relief="flat"
)
toggle.place(
    x=93.0,
    y=36.0,
    width=64.0,
    height=32.0
)

on_text = PhotoImage(file=relative_to_assets("on.png"))
onText = canvas.create_image(
    65.0,
    52.0,
    image=on_text
)

window.resizable(False, False)
window.mainloop()
