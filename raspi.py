import speech_recognition as sr
import firebase_admin
from firebase_admin import db
import keyboard

cred_obj = firebase_admin.credentials.Certificate("/home/ayush/projectA/large-languge-model-firebase-adminsdk-spyw1-321f207473.json")
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':"https://large-languge-model-default-rtdb.firebaseio.com/"})
ref = db.reference("/")

def takeCommand():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)

        command = recognizer.recognize_google(audio)
        print("You said:", command)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        command = "wenifuhwnevuw9eivuhnwsioefvjnk;wefnvw[eoifnvkefwepoi;flkedfr"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        command = "What do you think we should talk about"
    except TimeoutError:
        print("Timeout: No speech detected")
        command = "What do you think we should talk about"
    return command

while True:
    a = input("Enter a")
    if a == "a":
        command = takeCommand()
        ref.update({"input": command})