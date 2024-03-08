from pathlib import Path
import tkinter as tk
import pyttsx3

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def relative_to_assets(path: str) -> Path:
   return ASSETS_PATH / Path(path)

def yesNo(callback,text,type):
   engine.say("Do you want to "+type+"?")
   engine.runAndWait()
   
   def yes_button_clicked(win):
      win.destroy()
      callback(True,text)

   def no_button_clicked(win):
      win.destroy()
      callback(False,text)

   root = tk.Toplevel()
   root.geometry("300x175")
   root.configure(bg = "#E1E3E9")
   canvas = tk.Canvas(
      root,
      bg = "#E1E3E9",
      height = 175,
      width = 300,
      bd = 0,
      highlightthickness = 0,
      relief = "ridge"
   )
   canvas.place(x = 0, y = 0)

   button_image_1 = tk.PhotoImage(file=relative_to_assets("bl_no.png"))
   bl_no = tk.Button(
      root,
      image=button_image_1,
      borderwidth=0,
      highlightthickness=0,
      command=lambda: no_button_clicked(root),
      relief="flat"
   )
   bl_no.place(
      x=40.0,
      y=90.0,
      width=220.0,
      height=50.0
   )

   button_image_2 = tk.PhotoImage(file=relative_to_assets("bl_yes.png"))
   bl_yes = tk.Button(
      root,
      image=button_image_2,
      borderwidth=0,
      highlightthickness=0,
      command=lambda: yes_button_clicked(root),
      relief="flat"
   )
   bl_yes.place(
      x=40.0,
      y=30.0,
      width=220.0,
      height=50.0
   )

   root.resizable(False, False)
   root.mainloop()