import speech_recognition as sr
import firebase_admin
from firebase_admin import db
import keyboard
import datetime
from firebase_admin import credentials, initialize_app, storage
import os
cred_obj = firebase_admin.credentials.Certificate(r"C:\Users\Ayush\Downloads\large-languge-model-firebase-adminsdk-spyw1-321f207473.json")
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':"https://large-languge-model-default-rtdb.firebaseio.com/",'storageBucket': 'large-languge-model.appspot.com'})
ref = db.reference("/")
e = datetime.datetime.now()
def takeCommand():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            #recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)
        print("You said:", command)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        command = "wenifuhwnevuw9eivuhnwsioefvjnk;wefnvw[eoifnvkefwepoi;flkedfr"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        command = "What you think we should talk about"
    return command
while True:
    print("Commands : 1.therapy session report, 2.delete conversation")
    print("Press space")
    keyboard.wait("space")
    user_input = takeCommand()
    old_value = ref.get()["output"]
    ref.update({"input": user_input + " [Time:-{hour}:{minute}:{second}]".format(hour=e.hour,minute=e.minute,second=e.second)})
    new_value = ref.get()["output"]
    if user_input: 
        if "therapy session report" in user_input.lower():
            print("Creating Therapy Session Report")
            old_value = ref.get()["report"]
            while True:
                new_value = ref.get()["report"]
                if old_value != new_value:
                    source_blob_name = "example_report_with_heading.pdf"
                    bucket_name = "large-languge-model.appspot.com"
                    #The path to which the file should be downloaded
                    destination_file_name=r"C:\Users\Ayush\OneDrive\Desktop\GIT\TherapyLLM\example_report_with_heading.pdf"
                    assert os.path.isfile(destination_file_name)
                    bucket = storage.bucket()
                    blob = bucket.blob(source_blob_name)
                    blob.download_to_filename(destination_file_name)
                    break
    if user_input: 
        while True:
            if old_value!=new_value:
                break
            new_value = ref.get()["output"]
    print("OUTPUT: " + new_value)