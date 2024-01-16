from selenium import webdriver	 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time 
import speech_recognition as sr
import json
import firebase_admin
import os
import keyboard
from firebase_admin import db
cred_obj = firebase_admin.credentials.Certificate(r"C:\Users\vaida\Downloads\large-languge-model-firebase-adminsdk-spyw1-321f207473.json")
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':"https://large-languge-model-default-rtdb.firebaseio.com/"})
ref = db.reference("/")
data=ref.set({"output":"hi","input":"hi"})
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
import html
from gtts import gTTS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()
import subprocess
import openai
openai.api_key = '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'
messages = [ {"role": "system", "content":  
            "You are a intelligent assistant."} ] 
working_directory = r"C:\Users\vaida\text-generation-webui"
python_path = r"C:\Users\vaida\.conda\envs\textgen\python.exe"
script_path1 = r"C:\Users\vaida\OneDrive\Desktop\GIT\TherapyLLM\TherapyReport.py"
script_path2 = r"C:\Users\vaida\AppData\Local\ov\pkg\audio2face-2023.1.1\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server\test_client.py"
audio_file_path = r"C:\Users\vaida\text-generation-webui\audio_file_folder\welcome2.wav"
streaming_path = "/World/audio2face/PlayerStreaming"
script_path = r"server.py" 
model_path = r"C:\Users\vaida\text-generation-webui\models\Ayush2312_llama2-7B-1k-TherapyData"
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

    time.sleep(15)
    user = browser.find_elements(By.XPATH, '//*[@id="chat-input"]/label/textarea')

    try:
        while True:
            in_old = ref.get()["input"]
            out_old = ref.get()["output"]
            user_input = userinput(in_old) 
            while True:  
                if user_input: 
                    user_check = """AYUSHTEXT="{user_input}", check if this AYUSHTEXT means create therapy session report, if it means create therapy session report then reply me with "YES" otherwise reply with "NO" remember your reply should be only one word "YES" or "NO" """.format(user_input=user_input)
                    messages.append( 
                        {"role": "user", "content": user_check}, 
                    ) 
                    chat = openai.ChatCompletion.create( 
                        model="gpt-3.5-turbo", messages=messages 
                    ) 
                reply = chat.choices[0].message.content 
                #print(f"ChatGPT: {reply}") 
                if reply=="YES":
                    print("Creating Therapy Session Report")
                    subprocess.run(command1, shell=True)
                    user_input="Thanks for this conversation, Bye :)"
                break
            user[0].send_keys(user_input)
            userbtn = browser.find_element(By.XPATH, '//*[@id="Generate"]')
            userbtn.click()
            output1 = output(out_old)
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
    tts.save(r"C:\Users\vaida\text-generation-webui\audio_file_folder\welcome2.wav")
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
    os.remove(r"C:\Users\vaida\text-generation-webui\audio_file_folder\welcome2.wav")

def output(out_old):
    while True:
        time.sleep(1)
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
def userinput(in_old):
    print("waiting for input....")
    while True:
        time.sleep(1)
        in_new = ref.get()["input"]
        if in_new!= in_old:
            # print(out)
            break
    return in_new

run_server(working_directory, python_path, script_path, model_path)


