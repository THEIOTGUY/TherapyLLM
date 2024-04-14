# TherapyLLM
## Llama 2-7B Fine-Tuning on Therapy Dataset

### Overview :

This repository contains the code and resources for fine-tuning the Llama 2-7B language model on the Therapy dataset. The project aims to leverage state-of-the-art natural language processing (NLP) capabilities to enhance the understanding and generation of therapeutic content. This work is part of the final year project, demonstrating the application of advanced language models in the domain of mental health and therapy.

### Introduction :

The Real-Time Therapy Assistant combines the power of Llama 2-7B with a human-like animated character to enhance the therapeutic interaction experience. The visual aspect adds a personalized touch to the conversation, fostering a more engaging and supportive environment. Also it will create a personalized Therapy report based on the conversations

### Features :
* Real-Time Conversations: Engage in dynamic, responsive conversations with users.
* Context-Aware Responses: Utilize the context of the ongoing conversation to generate empathetic and relevant responses.
* Human Animation: Visually appealing animated character to enhance the user experience.
* Audio Interaction: Listen to users through the microphone and respond via speakers.
* Therapy Report Generation: Summarize the conversation into a comprehensive Therapy Report.
* User-Friendly Interface: Implement a visually appealing and intuitive user interface.

### USAGE :
* Run omniclientpython.py on remote laptop/PC and install and open omniclient on your computer, Enter the omniverse server code running in server into your omniverser client so you can see the animation in real-time
* If using raspberrypi then install ubuntu 23.10 server then git clone this repo and then run the following commands and then run raspberrypi_Client.py using sudo command.
```
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install jackd2
sudo apt-get install flac
pip install pyaudio
git clone https://github.com/THEIOTGUY/TherapyLLM.git
cd TherapyLLM
pip install -r requirementsRASPI.txt
```
### Proposed Design:
The study titled "AI-based Therapist using finetuned LLM" presents a new way to make large language models (LLMs) better for analyzing therapy data and providing remote therapeutic consultancy. It uses cutting-edge methods like 4-bit making smaller, Low-Rank Changing (LORA), and Cutting, Expert, and Tuning (PEFT) setups to make the model understand and respond for therapy tasks. We gathered and cleaned a dataset of 100k therapy talks from Hugging Face. (2023). jerryjalapeno/nart-100k-synthetic [Data set]. And we selected 1000 conversation samples for finetuning the model by data-processing technique and selecting samples from fields like depression, loneliness, anxiety, etc. We also made sure this data samples will be different from each other for better data diversity and quality. The dataset we processed for RAG (Retrieval Augmented Generation) is 807k samples by extracing each QnA pair from 100k therapy conversation samples, 807k therapy talks Hugging Face. (2023). Ayush2312/Therapydataset_formatted_807K [Data set] For a system called Retrieval-Augmented Generation (RAG) and FAISS for creating vectors. We converted this 807k QnA pairs into vector embedding so when a user asks a therapy related question the model will be given a similar sample from this 807k QnA based on the question asked along with the original question in the prompt (see Fig 1 for reference). We trained and improved model in a specific tech setup, worked on making it the best through testing with different datasets and prompts, and checked its success by looking at how precise and detailed it was as compared to the dataset. The aim was to make the Llama 2.7B LLM better at analyzing human emotional problems and giving appropiate replies just like a therapy consultant and by checking the impact of making it smaller i.e by making it use less memory footprint (GPU VRAM), using LORA wisely, using PEFT setups, and using the RAG system. The study looked to improve how the model performs, uses computer resources (GPU VRAM), and manages memory. Results showed a big boost in how well the model worked while keeping it efficient, showing the big chance of using fine-tuned LLMs for detailed tasks like therapy data analysis. This work helps move natural language processing forward and paves the way for more use of top language models for therapy-based apps. Model Structure: We used the Llama 2, a large model based on transformers that was already trained on a lot of text, known for understanding complex word patterns and meanings. We made the Llama 2 model better for therapy tasks by teaching it on special datasets, making it get the unique features and details. We added Low-Rank Adaptation (LoRA) LoRA circumvents the need to modify parameters within a pre-trained model and instead enables the application of a limited set of supplementary parameters. These supplementary parameters are transiently applied to the foundational model, effectively managing and directing its operational behavior. We made the Llama 2 model better by training it with datasets with mental health talks and trauma conversations. Training it on 1000 conversations took the model 200 minutes (3.33 hours) on a GPU. We split datasets into parts for training, testing, and validation, making the model better by using algorithms based on gradient descent and finding the best parameters through checks. We Evaluated the performance of the fine-tuned Llama 2 model using standard metrics such as relevance to dataset examples and comparing against baseline models to assess effectiveness.

### Working :
* The project uses Therapy Dataset to Fine-tune llama-2-7B which can be found here  [Therapy Dataset link](https://huggingface.co/datasets/Ayush2312/Therapydataset_formatted)
* After Fine-tuning the LLM we will use "https://github.com/oobabooga/text-generation-webui.git" for running the Fine-tune LLM, Also replace chat.py from modules folder from https://github.com/oobabooga/text-generation-webui.git with the chat.py given in repository
* We will use Omni-Verse Audio2Face for visual graphics (i.e Animations).
* We can use omniclientpython.py or raspberrypi_Client.py as input methods for LLM

### Webpage Screenshots:


![Screenshot 2024-04-08 222730](https://github.com/THEIOTGUY/TherapyLLM/assets/102857010/9929f10b-e838-4547-8429-323e19ebcc3b)

### Therapy Report : (Therapy Report will be created in pdf and will be ready to download)

Therapy Session Report:
Therapy Session Report
Client: Ayush
Date: 09 April 2024
Therapist: Suzan

Presenting Concerns: Ayush presented for therapy today reporting the death of a close friend last week. He expressed feeling a range of emotions including sadness, anger, and confusion.
Client Narrative: Ayush described his friend as being a very important person in his life. They shared many activities and confided in each other. He spoke about the suddenness of the death and how he is struggling to come to terms with it. Ayush also mentioned feeling overwhelmed by the emotions he is experiencing.
Assessment: Ayush is in the early stages of grief following the loss of his close friend. It is normal to experience a wide range of emotions during this time.
Treatment Plan:
Validation: The therapist validated Ayush's emotions and let him know that it is okay to feel sad, angry, confused, or any other emotions that come up.
Psychoeducation: The therapist provided Ayush with information about the grieving process and what to expect in the coming weeks and months.
Coping Skills: The therapist discussed coping skills that Ayush can use to manage his difficult emotions, such as relaxation techniques, journaling, and spending time with supportive loved ones.
Support System: The therapist encouraged Ayush to reach out to his support system for comfort and understanding.
Prognosis: With support and therapy, Ayush is expected to gradually heal from this loss. However, grief is a personal process and there is no set timeline for healing.
Next Steps: Ayush will be scheduled for a follow-up session in one week to discuss his progress and continue working through his grief.






