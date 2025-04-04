from numerizer import numerize
import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import os

engine = pyttsx3.init()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def TakeCommand():
        r = sr.Recognizer() # it recognize the speech
        with sr.Microphone() as source:
            print("Listening.....")
            speak("Give me command sir I'm Listening")
            r.pause_threshold = 1 
            audio = r.listen(source)
        try:
            print("Recognizing.....")
            speak("Recognizing")
            query = r.recognize_google(audio,language= 'en-US')
            return query
        
        except Exception as e:
            print(e)
            print("Say that again please.....")
            speak("Say that again please")
            return "None"

n = numerize(TakeCommand().lower())

c = int(n)
print(c)
print(type(c))