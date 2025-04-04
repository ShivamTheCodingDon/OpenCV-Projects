import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import os
import pyfirmata
from numerizer import numerize

pin = 9
port = "COM8"
board = pyfirmata.ArduinoNano(port)
LED = board.digital[pin]
LED.mode = pyfirmata.PWM

engine = pyttsx3.init()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

i = 1
while i > 0:
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

    if "led on" in TakeCommand().lower():
        LED.write(1)
    if "led off" in TakeCommand().lower():
        LED.write(0)
    if "jarvis bye" in TakeCommand().lower():
        speak('Have a nice day sir')
        i = 0
        globals()['i'] = i
        print(i)
    if "set the value of" in TakeCommand().lower():
        speak("Sir what value you want....")
        n = numerize(TakeCommand().lower())
        c = int(n)
        print(c)
        LED.write(c/100)
                                                                                    

    else:
        speak("Please say like  Hey jarvis and then your query")
