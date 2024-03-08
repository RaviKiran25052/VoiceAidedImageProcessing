import os
import pyttsx3
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from googletrans import LANGUAGES
from gtts import gTTS
from choice import yesNo

mykey = "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"
model = OpenAI(temperature=0.5, openai_api_key=mykey, model="gpt-3.5-turbo-instruct") # type: ignore

engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def summarize(text, lang):
   prompt = PromptTemplate(
      template = "give the text in {x} by summarizing the below text, within 50 to 60 words. text: {y}.",
      # template = "summarize this text within 30 words which was in {x}. text: {y}.",
      input_variables = ["x", "y"]
   )
   query = prompt.format(x=lang, y=text)
   translated_text = model(prompt=query)    
   return translated_text

def T2S(text,lan):
   length = len(text.split())
   if length > 50:
      print(f"\nThe text contains {length} words.")
      engine.say(f"The text contains {length} words.")
      engine.runAndWait()
      def willSummarize(result,text):
         if result:
            text = summarize(text, LANGUAGES[lan])
            print("\nThe summarized text is : ",text)
         audio = gTTS(text=text, lang=lan, slow=False)
         engine.say('the audio was saved...!')
         engine.runAndWait()
         audio.save("audio.mp3")
         os.system("start audio.mp3")
      yesNo(willSummarize,text,'Summarize')
   
   else:
      audio = gTTS(text=text, lang=lan, slow=False)
      engine.say('the audio was saved...!')
      engine.runAndWait()
      audio.save("audio.mp3")
      os.system("start audio.mp3")
