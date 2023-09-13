import os
import requests
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv(
    "AZURE_OPENAI_ENDPOINT"
)  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = "azure"
openai.api_version = "2023-05-15"  # this may change in the future

deployment_name = "gpt-35-turbo-16k"  # This will correspond to the custom name you chose for your deployment when you deployed a model.

# "functions": [
#     {
#       "name": "get_current_weather",
#       "description": "Get the current weather in a given location",
#       "parameters": {
#         "type": "object",
#         "properties": {
#           "location": {
#             "type": "string",
#             "description": "The city and state, e.g. San Francisco, CA"
#           },
#           "unit": {
#             "type": "string",
#             "enum": ["celsius", "fahrenheit"]
#           }
#         },
#         "required": ["location"]
#       }
#     }

functions = [
    {
        "name": "take_picture",
        "description": "Returns a picture taken with the robot's camera facing the direction the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "rotate_robot_body",
        "description": "Rotates the robot's body a certain number of degrees.",
        "parameters": {
            "type": "object",
            "properties": {
                "degrees": {
                    "type": "number",
                    "description": "The number of degrees to rotate the robot's body.",
                }
            },
            "required": ["degrees"],
        },
    },
    {
        "name": "rotate_robot_camera",
        "description": "Rotates the robot's camera a certain number of degrees.",
        "parameters": {
            "type": "object",
            "properties": {
                "degrees": {
                    "type": "number",
                    "description": "The number of degrees to rotate the robot's camera.",
                }
            },
            "required": ["degrees"],
        },
    },
    {
        "name": "move",
        "description": "Moves the robot a certain number of meters.",
        "parameters": {
            "type": "object",
            "properties": {
                "meters": {
                    "type": "number",
                    "description": "The number of meters to move the robot.",
                }
            },
            "required": ["meters"],
        },
    },
    {
        "name": "point_at_object",
        "description": "Shines the robot's light directly ahead of the robot.",
        "parameters": {},
    },
    {
        "name": "zoom_in",
        "description": "Zooms in the robot's camera.",
        "parameters": {},
    },
    {
        "name": "zoom_out",
        "description": "Zooms out the robot's camera.",
        "parameters": {},
    },
    {
        "name": "prompt_user_for_input",
        "description": "Prompts the user for input with a clarifying question.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask the user.",
                }
            },
            "required": ["question"],
        },
    },
    {
        "name": "end_session_with_success",
        "description": "Ends the session with success.",
        "parameters": {},
    },
    {
        "name": "end_session_with_failure",
        "description": "Ends the session with failure and a message describing why the session failed.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message describing why the session failed.",
                }
            },
            "required": ["message"],
        },
    },
    {
        "name": "vision_api_ocr",
        "description": "Returns the text in a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "vision_api_image_analysis_generic_caption",
        "description": "Returns a generic caption for a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "vision_api_image_analysis_dense_caption",
        "description": "Returns a dense caption for a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "vision_api_image_analysis_specific_location_bounding_boxes",
        "description": "Returns the bounding boxes for specific locations in a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "vision_api_face",
        "description": "Returns the faces in a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "vision_api_spatial_analysis",
        "description": "Returns the spatial analysis for a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "speech_api_text_to_speech",
        "description": "Returns the text to speech audio stream for a given string. This is used to make the robot's speakers play the given string.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to convert to speech.",
                }
            },
            "required": ["text"],
        },
    },
]

response = openai.ChatCompletion.create(
    engine=deployment_name,  # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
    messages=[
        {
            "role": "system",
            "content": "You control a robot that responds to the request of the user. You will take a series of actions to complete the tasks. The robot has a camera, and there are a 3 APIs you may call on the image taken from the robot's camera. You should decide the series of actions to take. The Optical Character Recognition (OCR) service extracts text from images. You can use the new Read API to extract printed and handwritten text from photos and documents. It uses deep-learning-based models and works with text on various surfaces and backgrounds. These include business documents, invoices, receipts, posters, business cards, letters, and whiteboards. The Image Analysis service extracts many visual features from images, such as objects, faces, adult content, and auto-generated text descriptions. Follow the Image Analysis quickstart to get started. The Face service provides AI algorithms that detect, recognize, and analyze human faces in images. Facial recognition software is important in many different scenarios, such as identity verification, touchless access control, and face blurring for privacy. The Spatial Analysis service analyzes the presence and movement of people on a video feed and produces events that other systems can respond to.",
        },
        {"role": "user", "content": "Find the lowest calorie item on the menu."},
    ],
)

print(response)

print(response["choices"][0]["message"]["content"])

# You are controlling a helpful and benevolent robot to serve human requests to the best of your ability in the most effective and efficient manner possible. The initial requests will not follow any strict template and may be extremely varied. They will be provided in natural speech. The information provided to you will be a list of messages which will detail what has happened so far in the session. You will have to keep track of a "Goal" (what the human currently wants to be accomplished). You will be given a list of "Functions" (all of the possible actions the robot can take and the list of actions you can choose from). You are to always choose the most appropriate action from the list of "Functions" informed by the current context and what has happened in the past in the message history. The "Goal" may be changed by feedback from the human user only.
# List of "functions":
# - Take a picture
# - Rotate robot body X degrees
# - Rotate robot camera X degrees
# - Move X meters
# - Point at object
# - Zoom in/out

# - Prompt user for input with clarifying question (and adjust goal if necessary)
# - End session with success
# - End session with failure

# - Vision API: OCR
# - Vision API: Image Analysis (Generic caption)
# - Vision API: Image Analysis (Dense caption)
# - Vision API: Image Analysis (Specific location bounding boxes)
# - Vision API: Face
# - Vision API: Spatial Analysis

# - Speech API: Text to Speech

# Example:
# user: "I am thirsty. I want to drink something.
