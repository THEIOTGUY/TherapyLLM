# TherapyLLM
## Llama 2-7B Fine-Tuning on Therapy Dataset

### Overview :

This repository contains the code and resources for fine-tuning the Llama 2-7B language model on the Therapy dataset. The project aims to leverage state-of-the-art natural language processing (NLP) capabilities to enhance the understanding and generation of therapeutic content. This work is part of the final year project, demonstrating the application of advanced language models in the domain of mental health and therapy.

### Introduction :

The Real-Time Therapy Assistant combines the power of Llama 2-7B with a human-like animated character to enhance the therapeutic interaction experience. The visual aspect adds a personalized touch to the conversation, fostering a more engaging and supportive environment.

### Features :
* Real-Time Conversations: Engage in dynamic, responsive conversations with users.
* Context-Aware Responses: Utilize the context of the ongoing conversation to generate empathetic and relevant responses.
* Human Animation: Visually appealing animated character to enhance the user experience.
* Audio Interaction: Listen to users through the microphone and respond via speakers.
* Therapy Report Generation: Summarize the conversation into a comprehensive Therapy Report.
* User-Friendly Interface: Implement a visually appealing and intuitive user interface.

### USAGE :
* Run omniclientpython.py on remote laptop/PC and install and open omniclient on your computer, Enter the omniverse server code running in server into your omniverser client so you can see the animation in real-time
* If using raspberrypi git clone this repo and then run the following commands and then run raspberrypi_Client.py using sudo command.
```
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
pip install pyaudio
git clone https://github.com/THEIOTGUY/TherapyLLM.git
cd TherapyLLM
pip install -r requirementsRASPI.txt
```

### Working :
* The project uses Therapy Dataset to Fine-tune llama-2-7B which can be found here  [Therapy Dataset link](https://huggingface.co/datasets/Ayush2312/Therapydataset_formatted)
* After Fine-tuning the LLM we will use "https://github.com/oobabooga/text-generation-webui.git" for running the Fine-tune LLM, Also replace chat.py from modules folder from https://github.com/oobabooga/text-generation-webui.git with the chat.py given in repository
* We will use Omni-Verse Audio2Face for visual graphics (i.e Animations).
* We can use omniclientpython.py or raspberrypi_Client.py as input methods for LLM









replace chat.py from modules folder from https://github.com/oobabooga/text-generation-webui.git with the chat.py given in repository

### Raspberrypi:
install ubuntu 23.10 server then create vnenv and then install pyaudio by : 
```
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
pip install pyaudio
```
pyaudio is necessary for speechrecognition library
