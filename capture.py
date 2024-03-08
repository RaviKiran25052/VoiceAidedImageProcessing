import time
import easyocr
import pyttsx3
import cv2
import pytesseract as pytesseract
from googletrans import Translator,LANGUAGES
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk
from choice import yesNo
from translate import lang_opt
from speak import T2S

engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

translator = Translator()
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Ravi\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

def relative_to_assets(path: str) -> Path:
   return ASSETS_PATH / Path(path)

def capture_image(vid,window):
   ret, frame = vid.read()
   if ret:
      cv2.imwrite("capture.png",frame)
      time.sleep(.1)
      engine.say('Image captured, processing for text...')
      engine.runAndWait()
      print("Image captured and saved as capture.png")  
   vid.release()
   window.destroy()
   I2T('capture.png')

def update_video(vid, canvas, window):
   ret, frame = vid.read()
   if ret:
      photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
      canvas.create_image(canvas.winfo_width()/2, (canvas.winfo_height()-80)/2, image=photo, anchor=tk.CENTER)
      canvas.photo = photo
   window.after(10, lambda: update_video(vid, canvas, window))

def identifyLang(img):
   percentages = []
   codes = ['en','te','hi']

   for code in codes:
      reader = easyocr.Reader([code],gpu=False)
      result = reader.readtext(img)

      pb = 0
      count = 0
      for items in result:
         _,_,score = items
         pb += score
         count +=1
      if count==0:
         break
      percentages.append([code, pb/count])
      # print(lang,percentages)
   if len(percentages) == 0:
      return False
   max_pair = max(percentages, key=lambda x: x[1])
   langCode = max_pair[0]
   if langCode == 'en':
      return [langCode]
   else:
      return ['en',langCode]
      
def I2T(img_path):
   
   langCodes = identifyLang(img_path)
   if not langCodes:
      time.sleep(.1)
      print('No text identified...!')
      engine.say('No text identified...!')
      engine.runAndWait()
      return
   reader = easyocr.Reader(langCodes)
   print(langCodes)
   result = reader.readtext(img_path)
   text = ' '.join([text[1] for text in result])
   print("The text was :\n" + text)
   
   ex = translator.detect(text)
   detected_lang = LANGUAGES[ex.lang]
   print("\nThe text was in: " + detected_lang)   
   time.sleep(.1)
   engine.say("The text was in: " + detected_lang)
   engine.runAndWait()
   
   def translatedText(tt,tl):
      text, lan = tt,tl
      print("\nTranslated text :\n",text)
      T2S(text, lan)
   
   def willTranslate(result,text):
      if result:
         lang_opt(text,ex.lang,translatedText)
      else:
         T2S(text,ex.lang)
   
   yesNo(willTranslate,text, 'Translate')

def oncamera():
   
   window = tk.Toplevel()

   window.geometry("700x500")
   window.configure(bg = "#E1E3E9")

   canvas = tk.Canvas(
      window,
      bg = "#E1E3E9",
      height = 500,
      width = 700,
      bd = 0,
      highlightthickness = 0,
      relief = "ridge"
   )
   canvas.place(x = 0, y = 0)

   vid = cv2.VideoCapture(0) 
   width, height = 750, 250
   vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
   vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
   _, frame = vid.read()
   opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
   captured_image = Image.fromarray(opencv_image)
   photo_image = ImageTk.PhotoImage(image=captured_image)

   button_image_1 = tk.PhotoImage(file=relative_to_assets("camera.png"))
   button_1 = tk.Button(
      window,
      image=button_image_1,   
      borderwidth=0,
      highlightthickness=0,
      background="#E1E3E9",
      command=lambda: capture_image(vid,window),
      relief="flat"
   )
   button_1.place(
      x=300.0,
      y=395.0,
      width=100.0,
      height=100.0
   )

   time.sleep(.1)
   engine.say('Capturing started...')
   engine.runAndWait()
   update_video(vid, canvas, window)
   window.resizable(False, False)
   window.mainloop()
