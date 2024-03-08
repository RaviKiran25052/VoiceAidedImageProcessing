from pathlib import Path
import tkinter as tk
import pyttsx3
from googletrans import Translator,LANGUAGES

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def lang_opt(text,lang,translated):
    
    def T2T(window, message, srcLang, destLang):
        trans = Translator()
        t = trans.translate(message, dest=destLang, src=srcLang)
        window.destroy()
        translated(t.text, destLang)
    
    lang_window = tk.Toplevel()
    lang_window.geometry("350x533")
    lang_window.configure(bg = "#E1E3E9")

    canvas = tk.Canvas(
        lang_window,
        bg = "#E1E3E9",
        height = 533,
        width = 350,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    button_image_1 = tk.PhotoImage(file=relative_to_assets("tamil.png"))
    tamil = tk.Button(
        lang_window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: T2T(lang_window,text,lang,'ta'),
        relief="flat"
    )
    tamil.place(
        x=50.0,
        y=435.0,
        width=250.0,
        height=50.0
    )

    button_image_2 = tk.PhotoImage(file=relative_to_assets("telugu.png"))
    telugu = tk.Button(
        lang_window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: T2T(lang_window,text,lang,'te'),
        relief="flat"
    )
    telugu.place(
        x=50.0,
        y=364.0,
        width=250.0,
        height=50.0
    )

    button_image_3 = tk.PhotoImage(file=relative_to_assets("hindi.png"))
    hindi = tk.Button(
        lang_window,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: T2T(lang_window,text,lang,'hi'),
        relief="flat"
    )
    hindi.place(
        x=50.0,
        y=293.0,
        width=250.0,
        height=50.0
    )

    button_image_4 = tk.PhotoImage(file=relative_to_assets("eng.png"))
    eng = tk.Button(
        lang_window,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: T2T(lang_window,text,lang,'en'),
        relief="flat"
    )
    eng.place(
        x=50.0,
        y=222.0,
        width=250.0,
        height=50.0
    )

    canvas.create_text(
        127.0,
        142.0,
        anchor="nw",
        text="Select_the\nLanguage:",
        fill="#000000",
        font=("SourceSansPro SemiBold", 20 * -1)
    )

    image_image_1 = tk.PhotoImage(file=relative_to_assets("statement.png"))
    image_1 = canvas.create_image(
        175.0,
        81.0,
        image=image_image_1
    )

    lang_window.resizable(False, False)
    lang_window.mainloop()
