from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver=webdriver.Chrome()
from time import sleep

# Open Scrapingbee's website
driver.get("http://127.0.0.1:7860/")

#x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chat-input > label > textarea")))
#x.click()
#x.send_keys("This text is send using Python code.")
#generate = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#Generate")))
#generate.click()
#css0 = "#chat > div > div:nth-child(2) > div.text > div.message-body > p"
#css = "#chat > div > div:nth-child({n}) > div.text > div.message-body > p"
def output(text):
    x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chat-input > label > textarea")))
    x.click()
    x.send_keys(text)
    generate = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#Generate")))
    generate.click()
    # = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css.format(n=n))))
    #print(query.text)

while True:
    text = input("Enter text")
    output(text)
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#sentiment = SentimentIntensityAnalyzer()
#text_1 = "i failed my exam"
#text_2 =  "my friend died"
#sent_1 = sentiment.polarity_scores(text_1)
#sent_2 = sentiment.polarity_scores(text_2)
#print("Sentiment of text 1:", sent_1)
#print("Sentiment of text 2:", sent_2)
    