import os
import requests
import json
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this may change in the future

deployment_name='gpt-35-turbo-16k' #This will correspond to the custom name you chose for your deployment when you deployed a model. 

response = openai.ChatCompletion.create(
    engine=deployment_name, # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
    messages=[
        {"role": "system", "content": "You control a robot that responds to the request of the user. You will take a series of actions to complete the tasks. The robot has a camera, and there are a 3 APIs you may call on the image taken from the robot's camera. You should decide the series of actions to take. The Optical Character Recognition (OCR) service extracts text from images. You can use the new Read API to extract printed and handwritten text from photos and documents. It uses deep-learning-based models and works with text on various surfaces and backgrounds. These include business documents, invoices, receipts, posters, business cards, letters, and whiteboards. The Image Analysis service extracts many visual features from images, such as objects, faces, adult content, and auto-generated text descriptions. Follow the Image Analysis quickstart to get started. The Face service provides AI algorithms that detect, recognize, and analyze human faces in images. Facial recognition software is important in many different scenarios, such as identity verification, touchless access control, and face blurring for privacy. The Spatial Analysis service analyzes the presence and movement of people on a video feed and produces events that other systems can respond to."},
        {"role": "user", "content": "Find the lowest calorie item on the menu."},
    ]
)

print(response)

print(response['choices'][0]['message']['content'])
