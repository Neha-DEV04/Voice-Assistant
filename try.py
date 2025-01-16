import pyttsx3
import json
import speech_recognition as sr
import datetime
import pyaudio
import random



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices)