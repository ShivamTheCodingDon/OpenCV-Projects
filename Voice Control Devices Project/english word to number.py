import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import os

engine = pyttsx3.init()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

res = ""

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

help_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0'
}
 
# initializing string
test_str = TakeCommand()
 
# printing original string
print("The original string is : " + test_str)
 

# Convert numeric words to numbers
# Using join() + split()
print("in try")
res = ''.join(help_dict[ele] for ele in test_str.split())
    
print(res)
    
    
