import pyttsx3
import speech_recognition as VoiceRec
from playsound import playsound
from Features import *
import datetime
import webbrowser
import os
import random
VoiceEng = pyttsx3.init('sapi5')
def Speak(SpeakData):
    VoiceEng.say(SpeakData) 
    VoiceEng.runAndWait()
def TakeCommand():
    VRProp = VoiceRec.Recognizer()
    with VoiceRec.Microphone() as source:
        VRProp.adjust_for_ambient_noise(source)
        VRProp.pause_threshold = 0.5
        Voice = VRProp.listen(source)
    Audio = VRProp.recognize_google(Voice,language='en-in')
    return Audio
def Listen():
    try:
        Audio = TakeCommand()   
        print("User Said : \n"+Audio)
        if 'wikipedia' in Audio.lower():
            print("Searching WikiPedia...")
            Speak("Searching WikiPedia")
            Content = Wiki(Audio)
            print(Content)
            Speak(Content)
        elif 'open youtube' in Audio.lower():
            webbrowser.open("youtube.com")
        elif 'play music' in Audio.lower():
            Music_Dir = "E:/EDM"
            Songs = os.listdir(Music_Dir)
            index = random.randint(0,len(Songs)-1)
            os.startfile(os.path.join(Music_Dir,Songs[index]))
        elif 'time' in Audio.lower():
            strTime = datetime.datetime.now().strftime("%H:%M")
            if int(strTime.split(":")[0]) < 12:
                AP = "a.m."
            else :
                AP = "p.m."
            print("The Time is " + strTime.split(":")[0] + " Hours " + strTime.split(":")[-1] + " Minutes " + " " + AP)
            Speak("The Time is " + strTime.split(":")[0] + " Hours " + strTime.split(":")[-1] + " Minutes " + " " + AP)
    except VoiceRec.UnknownValueError:
        print("Couldn't Understand....")
    except VoiceRec.RequestError:
        print("Internet Connection Error...")
def WakeWord():
    try:
        print("Giga Not Heard...")
        WakeWordCheck =  TakeCommand()
        if "hey giga" == WakeWordCheck.lower() or "giga" == WakeWordCheck.lower():
            Speak("Yes Sir")
            print("Listening...")
            playsound('D:/Projects/TOPSEC/AI_Voice_Assistant/Extra/Audio_WakeWord/WakeWordReactAudON.mp3')
            Listen()
            playsound('D:/Projects/TOPSEC/AI_Voice_Assistant/Extra/Audio_WakeWord/WakeWordReactAudOFF.mp3')
    except VoiceRec.UnknownValueError:
        print("Couldn't Understand....")
    except VoiceRec.RequestError:
        print("Internet Connection Error...")
Speak("Powering Up")
Speak("All Primary System Online")
Speak("Welcome back")
Time = int(datetime.datetime.now().hour)
if Time >= 0 and Time < 12:
    Speak("Good Morning Sir")
elif Time >= 12 and Time < 17:
    Speak("Good Afternoon Sir")
else:
    Speak("Good Evening Sir")
while (1):
    WakeWord()