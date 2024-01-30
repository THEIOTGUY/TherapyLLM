from selenium import webdriver	 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import speech_recognition as sr
import json
import firebase_admin
import os
import shutil
from firebase_admin import db
cred_obj = firebase_admin.credentials.Certificate(r"firebasejson\large-languge-model-firebase-adminsdk-spyw1-321f207473.json")
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':"https://large-languge-model-default-rtdb.firebaseio.com/"})
ref = db.reference("/")
data = ref.set({"output":"hi","input":"hi","report":"er235ge","DELETE":"sdfuhsefuih"})
from selenium.webdriver.common.keys import Keys 
import html
from gtts import gTTS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()
import subprocess
from selenium.common.exceptions import TimeoutException
import argparse
ominiverse = False
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Omniverse Audio2Face')
# Add a command-line argument to toggle the variable
parser.add_argument('--omniverse', action='store_true', help='Toggle omniverse to True')

# Parse the command-line arguments
args = parser.parse_args()

# Update the variable based on the command-line argument
if args.omniverse:
    ominiverse = True

# Rest of your code
print(f'Launching with Omniverse Audio2Face')
working_directory = r"text-generation-webui"
python_path = r"C:\Users\Ayush\anaconda3\envs\LLM\python.exe"
script_path1 = r"TherapyReport.py"
script_path2 = r"C:\Users\Ayush\AppData\Local\ov\pkg\audio2face-2023.1.1\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server\test_client.py"
audio_file_path = r"text-generation-webui\audio_file_folder\welcome2.wav"
streaming_path = "/World/audio2face/PlayerStreaming"
script_path = r"server.py" 
model_path = r"models\Ayush2312_llama2-7B-1k-TherapyData"
command1 = [python_path, script_path1]
command2 = [python_path, script_path2, audio_file_path, streaming_path]
def takeCommand():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)

        command = recognizer.recognize_google(audio)
        print("You said:", command)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        command = ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        command = "What you think we should talk about"

    return command
def run_server(working_directory, python_path, script_path, model_path):

    process = subprocess.Popen(f'cd /d "{working_directory}" && {python_path} {script_path} --model "{model_path}" --load-in-4bit --use_double_quant --share',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    time.sleep(40)
    browser = webdriver.Firefox() 
    browser.get('http://127.0.0.1:7860/')
    user = WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chat-input"]/label/textarea')))

    try:
        while True:
            while True:
                in_old = ref.get()["input"]
                out_old = ref.get()["output"]
                delete_old = ref.get()["DELETE"]
                user_input = userinput(in_old,browser,delete_old) 
                if user_input: 
                    if "therapy session report" in user_input.lower():
                        print("Creating Therapy Session Report")
                        subprocess.run(command1, shell=True)
                        ref.update({"output":"Therapy session report has been created"})
                        break
                    if "delete conversation" in user_input.lower():
                        print("deleting conversations")
                        directory_to_delete1 = 'text-generation-webui\\logs\\chat\\Assistant'
                        directory_to_delete2 = 'text-generation-webui\\logs\\chat\\AI'
                        # Check if the directory exists before attempting to delete
                        if os.path.exists(directory_to_delete1) or os.path.exists(directory_to_delete2):
                            try:
                                # Attempt to remove the directory and its contents
                                shutil.rmtree(directory_to_delete1)
                                shutil.rmtree(directory_to_delete2)
                                print(f"Directory '{directory_to_delete1}' successfully deleted.")
                            except Exception as e:
                                print(f"Error deleting directory: {e}")
                        else:
                            print(f"Directory '{directory_to_delete1}' does not exist.")
                        browser.refresh()
                        ref.update({"output":"Previous Conversations has been deleted"})
                user = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chat-input"]/label/textarea')))
                user.send_keys(user_input)
                userbtn = browser.find_element(By.XPATH, '//*[@id="Generate"]')
                userbtn.click()
                output1 = output(out_old)
                if ominiverse == True:
                    get_tts(output1,user_input)

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print("Exiting script...")
        process_name = "python.exe"

        # Employing the taskkill command to terminate the process
        result = os.system(f"taskkill /f /im {process_name}")

def get_tts(output1,user_input):
    #output = GoogleTranslator(source='auto', target='hi').translate(output)
    tts = gTTS(output1)
    tts.save(r"text-generation-webui\audio_file_folder\welcome2.wav")
    print("got tts")
    text = " INPUT : ", user_input + " ,OUTPUT : " + output1
    sent_1 = sentiment.polarity_scores(text)
    neg = float(sent_1["neg"])
    pos = float(sent_1["pos"])
    text = {"a2f_instance": "/World/audio2face/CoreFullface", "emotions": {"joy": 0, "sadness": 0}}
    text["emotions"]["joy"] = pos
    text["emotions"]["sadness"] = neg
    print("sending emotions")
    text = json.dumps(text)
    text1 = text.replace("\"", "\\\"")
    wholetext = "curl -X \"POST\" \ \"http://localhost:8011/A2F/A2E/SetEmotionByName\" \ -H \"accept: application/json\" \ -H \"Content-Type: application/json\" \ -d \"{}\"".format(text1)
    os.system(wholetext)
    print("emotions sent")
    subprocess.run(command2, shell=True)
    os.remove(r"text-generation-webui\audio_file_folder\welcome2.wav")

def output(out_old):
    while True:
        #time.sleep(1)
        out = ref.get()["output"]
        if out_old != out:
            # print(out)
            break 
    try:
        out = html.unescape(out)
    except Exception as e:
        print(f"Error while unescaping HTML: {e}")
    
    print(out)
    return out
def userinput(in_old,browser,delete_old):
    print("Commands : 1.therapy session report, 2.delete conversation")
    print("waiting for input....")
    while True:
        #time.sleep(1)
        in_new = ref.get()["input"]
        delete_new = ref.get()["DELETE"]
        time.sleep(0.5)
        if in_new!= in_old:
            # print(out)
            break
        if delete_new!= delete_old:
            print("deleting conversations")
            directory_to_delete1 = 'text-generation-webui\\logs\\chat\\Assistant'
            directory_to_delete2 = 'text-generation-webui\\logs\\chat\\AI'
            # Check if the directory exists before attempting to delete
            if os.path.exists(directory_to_delete1) or os.path.exists(directory_to_delete2):
                try:
                    # Attempt to remove the directory and its contents
                    shutil.rmtree(directory_to_delete1)
                    shutil.rmtree(directory_to_delete2)
                    print(f"Directory '{directory_to_delete1}' successfully deleted.")
                except Exception as e:
                    print(f"Error deleting directory: {e}")
            else:
                print(f"Directory '{directory_to_delete1}' does not exist.")
            browser.refresh()
            ref.update({"output":"Previous Conversations has been deleted"})
    return in_new

run_server(working_directory, python_path, script_path, model_path)


