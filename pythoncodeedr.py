import firebase_admin
from gtts import gTTS
import os
from firebase_admin import db
import keyboard
import speech_recognition as sr  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()
driver=webdriver.Chrome()
from time import sleep
# Open Scrapingbee's website
driver.get("http://localhost:8011/docs")
cred_obj = firebase_admin.credentials.Certificate(r"C:\Users\vaida\Downloads\gen-lang-client-0134427173-firebase-adminsdk-vdatl-34e7edafaa.json")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://gen-lang-client-0134427173-default-rtdb.firebaseio.com'
	})
ref = db.reference("/")
o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#operations-Audio2Emotion-set_a2e_emotion_by_name_A2F_A2E_SetEmotionByName_post > div.opblock-summary.opblock-summary-post > button > span.opblock-summary-path > a > span"))).click()
y = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#operations-Audio2Emotion-set_a2e_emotion_by_name_A2F_A2E_SetEmotionByName_post > div.no-margin > div > div.opblock-section > div.opblock-section-header > div.try-out > button"))).click()
x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#operations-Audio2Emotion-set_a2e_emotion_by_name_A2F_A2E_SetEmotionByName_post > div.no-margin > div > div.opblock-section > div.opblock-section.opblock-section-request-body > div.opblock-description-wrapper > div > div > div > textarea")))
x.click()
x.clear()
text = text = """{
        "a2f_instance": "/World/audio2face/CoreFullface",
        "emotions": {
            "joy": 0,
            "sadness": 0
        }
        }"""
x.send_keys(text)
x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#operations-Audio2Emotion-set_a2e_emotion_by_name_A2F_A2E_SetEmotionByName_post > div.no-margin > div > div.execute-wrapper > button"))).click()

def get_value():
    # Usage example
    output = ref.get()
    output = output["output"]
    output = str(output)
    output = output.removesuffix("You:")
    return output
def get_tts(output):
    tts = gTTS(output)
    try:
        os.remove(r"C:\Users\vaida\Downloads\folderr2\welcome2.wav")
    except:
        tts.save(r"C:\Users\vaida\Downloads\folderr2\welcome2.wav")
        os.system(r"python C:\Users\vaida\AppData\Local\ov\pkg\audio2face-2023.1.1\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server\test_client.py C:\Users\vaida\Downloads\folderr2\welcome2.wav /World/audio2face/PlayerStreaming")
    try:
        os.remove(r"C:\Users\vaida\Downloads\folderr2\welcome2.wav")
    except:
        print("file not found")
old_output = get_value()

def speech_to_text():
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Speak:")                                                                                   
        audio = r.listen(source)
    try:
        a = r.recognize_google(audio)
        print("You said : " + a)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    if 'a' in locals():
        return a
def emotion_send(text):
    x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#operations-Audio2Emotion-set_a2e_emotion_by_name_A2F_A2E_SetEmotionByName_post > div.no-margin > div > div.opblock-section > div.opblock-section.opblock-section-request-body > div.opblock-description-wrapper > div > div > div > textarea")))
    x.click()
    x.clear()
    x.send_keys(text)
    x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#operations-Audio2Emotion-set_a2e_emotion_by_name_A2F_A2E_SetEmotionByName_post > div.no-margin > div > div.btn-group > button.btn.execute.opblock-control__btn"))).click()
def get_input():
    input = ref.get()
    input =input["input"]
    input = input.removeprefix("This is a conversation with your Assistant. It is a computer program designed to help you with various tasks such as answering questions, providing recommendations, and helping with decision making. You can ask it anything you want and it will do its best to give you accurate and relevant information")
    input = input.removesuffix("Assistant:")
    print(input)
    return input
while True:
    output = get_value()
    input = get_input()
    if output != old_output:
        print(output)
        sent_1 = sentiment.polarity_scores(input + output)
        print("this is the text : ",input + output)
        print(sent_1)
        neg = float(sent_1["neg"])+0.3
        pos = float(sent_1["pos"])+0.3
        text = """{{
        "a2f_instance": "/World/audio2face/CoreFullface",
        "emotions": {{
            "joy": {pos},
            "sadness": {neg}
        }}
        }}""".format(neg=neg,pos=pos)
        print(text)
        emotion_send(text)

        get_tts(output)
        old_output = output
    #if keyboard.read_key() == "space":
        #print("space key pressed")
        #output = speech_to_text()
        #get_tts(output)
        #old_output = output