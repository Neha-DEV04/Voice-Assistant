# import pyttsx3 #use this for windows
import json
import speech_recognition as sr
import datetime
# import pyaudio
import random
import wikipedia
import webbrowser
import time
from gtts import gTTS
import pygame
import os

wikipedia.set_lang('en')

# Use this for windows
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice' , voices[1].id)
# engine.setProperty('rate',175)

stop_flag = False
is_sleeping = False

with open('intents.json', 'r') as file:
    intents = json.load(file)["intents"]
    

def speak(audio):
    # Use this for windows
    # engine.say(audio)
    # engine.runAndWait()
    tts = gTTS(text=audio, lang='en')
    tts.save("temp.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
def get_user_input():
    r=sr.Recognizer()
    r.pause_threshold = 1
    r.energy_threshold = 290
    while True:
        with sr.Microphone()as mic:
            print("Listening....")        
            audio = r.listen(mic)
            
        try:
            query = r.recognize_google(audio, language='en-in')
            return query
        except Exception as e :
            speak("Sorry!! I did not understand that. Could you please reapeat?")
            
        
        
    
    
# def intent_recognition(user_input):
#     for intent in intents:
#         for example in intent["examples"]:
#             if example.lower() in user_input.lower():
#                 return intent
#     return None

def intent_recognition(user_input):
    best_intent = None
    max_match_count = 0
    
    for intent in intents:
        match_count = 0
        
        for example in intent["examples"]:
            if example.lower() in user_input.lower():
                match_count += 1
        
        if match_count > max_match_count:
            max_match_count = match_count
            best_intent = intent

    return best_intent

    
def stop_Evio():
    speak('Shutting down Evio!')
    os.remove('./temp.mp3')
    global stop_flag
    stop_flag = True


def sleep_Evio():
    global is_sleeping
    is_sleeping = True
    speak("Going to sleep! Wake me up by calling my name!")



def wake_Evio():
    global is_sleeping
    r = sr.Recognizer()
    r.pause_threshold = 1
    r.energy_threshold = 290
    
    while is_sleeping:
        with sr.Microphone() as mic:
            print("Listening for wake word....")
            audio = r.listen(mic)
            print(audio)
            query = r.recognize_google(audio, language='en-in')
            print(query)
        
        try:
            query = r.recognize_google(audio, language='en-in')
            print(query)
            # wake-word is evo as the recognizer is not recognising evio, after the wake-word
            #being renamed to evo it responds to evio.
            if "evo" in query.lower():
                is_sleeping = False
                speak("Hey! I am up. What can I do for you?")
        except Exception as e:
            pass


def search_wikipedia():
    speak("What do you want me to search?")
    query = get_user_input()
    speak("Searching Wikipedia...")
    query = query.replace("on wikipedia", "")
    print(query)
    try:
        result = wikipedia.summary(query, sentences=3)
        speak("According to Wikipedia")
        speak(result)
        pass
    
    except wikipedia.exceptions.PageError as e:
        speak("I couldn't find any information on Wikipedia for that query.")
        


def search_youtube():
    speak("What do you want me to search?")
    query = get_user_input()
    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    
    print(query)
    try:
        webbrowser.open(youtube_url)
        
        pass
    
    except webbrowser.Error as e:
        speak("I couldn't search it on YouTube.")
        



def search_google():
    speak("What do you want me to search?")
    query = get_user_input()
    google_url = f"https://www.google.com/search?q={query}"
    
    print(query)
    try:
        webbrowser.open(google_url)
        
        pass
    
    except webbrowser.Error as e:
        speak("I couldn't connect to Google.")
        

    

    
    
def get_time():
    strTime = datetime.datetime.now().strftime("%H:%M")
    speak(f"The time is {strTime}")




# def set_timer():
#     speak("Sure! Please specify the duration for the timer!")
#     say = ''
    
#     try:
#         user_input = get_user_input().lower()
#         print(user_input)
#         if "minutes" or "minute" in user_input:
#             user_input = user_input.replace(" minutes", "")
#             duration_mins = int(user_input)*60
#             min = "minutes"
            
#         if "hours" or "hour" in user_input:
#             user_input = user_input.replace(" hours", "")
#             duration_hours = int(user_input)*360
#             hr = "hours"
            
#         if "seconds" or "second" in user_input:
#             user_input = user_input.replace(" seconds", "")
#             duration_secs = int(user_input)
#             sec = "seconds"
            
        
#         duration = duration_mins + duration_hours + duration_secs
#         say = min + hr + sec
                
#     except:
#         speak("Could not set a timer!")
#         pass
            

#     speak(f"Timer set for {user_input} {say}. I will notify you when it's time.")
#     print("Waiting for timer!!")
#     time.sleep(duration)
#     speak("Timer has ended. Time's up!")
def set_timer():
    speak("Sure! Please specify the duration for the timer in seconds, minutes, or hours.")

    try:
        user_input = get_user_input().lower()
        print(user_input)

        duration = 0
        

        words = user_input.split()
        for i in range(0, len(words), 2):
            value = int(words[i])
            unit = words[i + 1]

            if "minute" in unit:
                duration += value * 60
                
            elif "hour" in unit:
                duration += value * 3600
                
            elif "second" in unit:
                duration += value

        if duration > 0:
            speak(f"Timer set for {user_input}. I will notify you when it's time.")
            print("Waiting for timer!!")
            time.sleep(duration)
            speak("Timer has ended. Time's up!")
        else:
            speak("Could not set a timer. Please specify a valid duration.")

    except Exception as e:
        speak("Could not set a timer!")




mapping = {
    "search_wikipedia": search_wikipedia,
    "get_time": get_time,
    "stop_Evio": stop_Evio,
    "search_google": search_google,
    "search_youtube": search_youtube,
    "sleep_Evio": sleep_Evio,
    "set_timer": set_timer,
    
}
if __name__ == "__main__":
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<17:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am Evio, your voice assistant! How can i help you today?")
    
    while not stop_flag:
        if not is_sleeping:
            user_input = get_user_input()
            print(user_input)
            recognized_intent = intent_recognition(user_input)
            print(recognized_intent)
            if recognized_intent:
            
                if "responses" in recognized_intent:
                    responses = recognized_intent['responses']
                    respond = random.choice(responses) 
                    speak(respond)
                if "action" in recognized_intent:
                    action = recognized_intent["action"]
                    
                    if action in mapping:
                        mapping[action]()
                        
                        if action != "stop_Evio" and action != "sleep_Evio":
                            sleep_Evio()
                            
                    else:
                        speak("I dont know how to do this!")
                        sleep_Evio()
                       
        else: 
            wake_Evio()
        