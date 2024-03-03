import speech_recognition as sr
import firebase_admin
from firebase_admin import db
import RPi.GPIO as GPIO
import os
import subprocess
import random
import string
import pygame
# Initialize the Pygame mixer module
pygame.mixer.init()
cred_obj = firebase_admin.credentials.Certificate("/home/ayush/projectA/large-languge-model-firebase-adminsdk-spyw1-321f207473.json")
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': "https://large-languge-model-default-rtdb.firebaseio.com/"})
ref = db.reference("/")
from gtts import gTTS
def takeCommand():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)
        print("You said:", command)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        random_alphabets = ''.join(random.choices(string.ascii_lowercase, k=10))  # Generate a random string of 10 lowercase alphabets
        command = f"wenifuhwnevuw9eivuhnwsioefvjnk;wefnvw[eoifnvkefwepoi;flkedfr{random_alphabets}"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        command = "What do you think we should talk about"
    return command

# Set up GPIO for the touch sensor
TOUCH_SENSOR_PIN = 17  # Replace with the GPIO pin connected to your touch sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN)
def output_(old_output):
    print("waiting for input....")
    while True:
        new_output = ref.get()["output"]
        if new_output != old_output:
            old_output = new_output
            break
    return new_output
def speak(output):
    language = 'en'

    # Adjusting parameters and creating gTTS object
    tts = gTTS(text=output, lang=language, slow=False)

    # Save the audio in a temporary WAV file
    temp_wav_file = "temp_audio.wav"
    tts.save(temp_wav_file)

    # Load the audio file
    pygame.mixer.music.load(temp_wav_file)

    # Set the volume level (value between 0.0 and 1.0, where 0.0 is silent and 1.0 is maximum volume)
    pygame.mixer.music.set_volume(1.0)  # Example: Set volume to 50%

    # Play the loaded audio
    pygame.mixer.music.play()
while True:
    print("Hold down touch sensor to start listening")
    
    # Wait for the touch sensor to be pressed
    while not GPIO.input(TOUCH_SENSOR_PIN):
        pass
    
    # Check if the touch sensor is still being pressed
    while GPIO.input(TOUCH_SENSOR_PIN):
        command = takeCommand()
        old_output = ref.get()["output"]
        ref.update({"input": command})
        output = output_(old_output)
        speak(output)
    print("Touch sensor released. Listening stopped.")
