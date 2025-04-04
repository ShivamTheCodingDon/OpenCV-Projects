import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import os
import pyfirmata
from numerizer import numerize
import cv2
from time import sleep
from cvzone.HandTrackingModule import HandDetector
import time


pin = 6
buzz_pin = 9
led_pin = 8
port = "COM8"
board = pyfirmata.ArduinoNano(port)
LED = board.digital[pin]
LED.mode = pyfirmata.PWM
BUZZ = board.digital[buzz_pin]
BUZZ.mode = pyfirmata.PWM 

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

    def time_():
        Time = datetime.datetime.now().strftime("%I:%M:%S") # for 12 hrs
        speak("The Current time is")
        speak(Time)

    def date_():
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        speak("The current date is")
        speak(day)
        speak(month)
        speak(year)

    def wishme():
        speak("Welcome back DON!")
        time_()
        date_()
    
    #Greetings
    
    hour = datetime.datetime.now().hour
    
    if hour >= 6 and hour < 12:
        speak("Good Morning Sir!")
        Jarviser_()
    elif hour >= 12 and hour < 18:
        speak("Good afternoon Sir!")
        Jarviser_()
    elif hour >= 18 and hour < 24:
        speak("Good Evening Sir!")
        Jarviser_()
    else:
        speak("Good Night Sir!")
        Jarviser_()
        speak("Sweet dreams sir!")

    def Jarviser_():
        speak("Jarvis at your service. Please tell me how can I help you today?")

    if "hey jarvis" or "hello jarvis" in TakeCommand().lower():
        wishme()
        if "i wanna control devices" or "i wanna control my home devices" in TakeCommand().lower():
            speak("okay sir!")
            speak("you want to control your devises by hand gesture or voice control")
            if "by hand gesture" or "hand gesture" or "by hand":
                cap = cv2.VideoCapture(0)
                detector = HandDetector(detectionCon=0.8, maxHands=2)
                pTime = 0
                
                while True:
                    success, img = cap.read()
                    hands, img = detector.findHands(img)  # With Draw
                    # hands = detector.findHands(img, draw=False)  # No Draw

                    if hands:
                        # Hand 1
                        hand1 = hands[0]
                        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
                        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
                        centerPoint1 = hand1["center"]  # center of the hand cx,cy
                        handType1 = hand1["type"]  # Hand Type Left or Right

                        
                        fingers1 = detector.fingersUp(hand1)
                        if len(hands) == 2:
                            hand2 = hands[1]
                            lmList2 = hand2["lmList"]
                            handType2 = hand2["type"]
                        
                            if handType1 == "Right":
                                if fingers1[2] == 0 and fingers1[3] == 0:
                                    board.digital[pin].write(0)
                                if fingers1[3] == 0 and fingers1[2] == 1:
                                    BUZZ.write(0)
                                if fingers1[4] == 0:
                                    board.digital[led_pin].write(fingers1[3])

                                
                            
                            if handType2 == "Left" and fingers1[1] == 1 and fingers1[3] == 0:
                                length, info, img = detector.findDistance(lmList2[4][0:2], lmList2[8][0:2], img) # with draw
                                lendis = int(length)
                                if lendis <= 15 :
                                    if fingers1[2] == 0:
                                        LED.write(0)
                                    BUZZ.write(0)
                                for i in range(15, lendis, 30):
                                    if fingers1[1] == 1 and fingers1[2] == 0:
                                        LED.write(i/130)
                                    elif fingers1[2] == 1:
                                        BUZZ.write(i/130)
                                    #print(i)
                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime

                    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                                3, (255, 0, 0), 3)

                    cv2.imshow("Image", img)
                    cv2.waitKey(1)

            elif "by voice control" or "voice control" in TakeCommand().lower():
                if "led on" in TakeCommand().lower():
                    LED.write(1)
                if "led off" in TakeCommand().lower():
                    LED.write(0)
                if "set the value of" in TakeCommand().lower():
                    speak("Sir what value you want....")
                    n = numerize(TakeCommand().lower())
                    c = int(n)
                    print(c)
                    LED.write(c/100)

    if "jarvis bye" in TakeCommand().lower():
                    speak('Have a nice day sir')
                    i = 0
                    globals()['i'] = i