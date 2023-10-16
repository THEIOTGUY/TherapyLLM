import httpx
import asyncio
import html
import json
import sys
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os
import time
import keyboard
sentiment = SentimentIntensityAnalyzer()
import keyboard
# import firebase_admin
# from firebase_admin import db
# def initialize_firebase():
#     cred_obj = firebase_admin.credentials.Certificate(r"C:\Users\vaida\Downloads\gen-lang-client-0134427173-firebase-adminsdk-vdatl-34e7edafaa.json")
#     default_app = firebase_admin.initialize_app(cred_obj, {
#         'databaseURL':'https://gen-lang-client-0134427173-default-rtdb.firebaseio.com'
#     })
#     return db.reference("/")
import websockets

#For local streaming, the websockets are hosted without ssl - ws://
HOST = 'localhost:5005'
URI = f'ws://{HOST}/api/v1/chat-stream'

# For reverse-proxied streaming, the remote will likely host with ssl - wss://
# URI = 'wss://your-uri-here.trycloudflare.com/api/v1/stream'
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)
    try:
        a = r.recognize_google(audio)
        print("You said: " + a)
        return a
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

async def make_request():
    async with httpx.AsyncClient() as client:
        url = 'http://localhost:8011/A2F/A2E/SetEmotionByName'
        response = await client.post(url, json=text)
        return response
def get_tts(output1):
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
    os.system(r"python C:\Users\vaida\AppData\Local\ov\pkg\audio2face-2023.1.1\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server\test_client.py C:\Users\vaida\text-generation-webui\audio_file_folder\welcome2.wav /World/audio2face/PlayerStreaming")
    os.remove(r"C:\Users\vaida\text-generation-webui\audio_file_folder\welcome2.wav")
async def run(user_input, history):
    # Note: the selected defaults change from time to time.
    request = {
        'user_input': user_input,
        'max_new_tokens': 250,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,
        'history': history,
        'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': 'Example',
        'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
        'your_name': 'You',
        # 'name1': 'name of user', # Optional
        # 'name2': 'name of character', # Optional
        # 'context': 'character context', # Optional
        # 'greeting': 'greeting', # Optional
        # 'name1_instruct': 'You', # Optional
        # 'name2_instruct': 'Assistant', # Optional
        # 'context_instruct': 'context_instruct', # Optional
        # 'turn_template': 'turn_template', # Optional
        'regenerate': False,
        '_continue': False,
        'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'grammar_string': '',
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'custom_token_bans': '',
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    async with websockets.connect(URI, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            match incoming_data['event']:
                case 'text_stream':
                    yield incoming_data['history']
                case 'stream_end':
                    return


async def print_response_stream(user_input, history):
    cur_len = 0
    output1 = ''
    print("Thinking...")
    async for new_history in run(user_input, history):
        cur_message = new_history['visible'][-1][1][cur_len:]
        cur_len += len(cur_message)
        #print(html.unescape(cur_message), end='')
        output = html.unescape(cur_message)
        output1 = output1 + output
        if output == "." and output1.count("") > 200 or output1.count("") > 350:
            print(output1)
            get_tts(output1)
            print("Line ________________")
            output1 = ''
        sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.
    print(output1)
    try:
        output1 = "\n".join(x for x in output1.splitlines() if "USER:" not in x)
        get_tts(output1)
    except:
        pass
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)
    try:
        s = r.recognize_google(audio)
        print("You said: " + s)
        return s
    except sr.UnknownValueError:
        print("Could not understand audio")
        user_input = input("Enter Prompt")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return user_input
if __name__ == '__main__':
    while True:
        event = keyboard.read_event()
        if event.name == "play/pause media":
            user_input = speech_to_text()
            # if keyboard.read_key() == "play/pause media":
            #     user_input = speech_to_text()
            # Basic example
            history = {'internal': [], 'visible': []}

            # "Continue" example. Make sure to set '_continue' to True above
            # arr = [user_input, 'Surely, here is']
            # history = {'internal': [arr], 'visible': [arr]}

            asyncio.run(print_response_stream(user_input, history))
        else:
            history = {'internal': [], 'visible': []}
            user_input = input("Enter : ")
            # "Continue" example. Make sure to set '_continue' to True above
            # arr = [user_input, 'Surely, here is']
            # history = {'internal': [arr], 'visible': [arr]}

            asyncio.run(print_response_stream(user_input, history))


