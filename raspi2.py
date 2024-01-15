import speech_recognition as sr
import firebase_admin
from firebase_admin import db
import RPi.GPIO as GPIO
import keyboard

cred_obj = firebase_admin.credentials.Certificate("/home/ayush/projectA/large-languge-model-firebase-adminsdk-spyw1-321f207473.json")
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': "https://large-languge-model-default-rtdb.firebaseio.com/"})
ref = db.reference("/")

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
        command = ".."
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        command = "What do you think we should talk about"
    return command

# Set up GPIO for the touch sensor
TOUCH_SENSOR_PIN = 17  # Replace with the GPIO pin connected to your touch sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN)

while True:
    print("Hold down touch sensor to start listening")
    
    # Wait for the touch sensor to be pressed
    while not GPIO.input(TOUCH_SENSOR_PIN):
        pass
    
    # Check if the touch sensor is still being pressed
    while GPIO.input(TOUCH_SENSOR_PIN):
        command = takeCommand()
        ref.update({"input": command})
    
    print("Touch sensor released. Listening stopped.")
