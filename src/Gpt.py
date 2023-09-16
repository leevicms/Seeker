import os
import requests
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv(
    "OPENAI_API_BASE"
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
        "name": "send_picture_to_user",
        "description": "Sends a picture to the user. The picture is taken with the robot's camera facing the direction the camera is currently facing.",
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
        "description": "Rotates the robot's camera to center in frame a given bounding box defined by dimensions x, y, w, and h.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "number",
                    "description": "The x coordinate of the bounding box of the object.",
                },
                "y": {
                    "type": "number",
                    "description": "The y coordinate of the bounding box of the object.",
                },
                "w": {
                    "type": "number",
                    "description": "The w coordinate of the bounding box of the object.",
                },
                "h": {
                    "type": "number",
                    "description": "The h coordinate of the bounding box of the object.",
                },
            },
            "required": ["x", "y", "w", "h"],
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
        "name": "end_session_with_success",
        "description": "Ends the session with success. This should be called when the user's goal has been achieved and the human user is satisfied.",
        "parameters": {},
    },
    {
        "name": "end_session_with_failure",
        "description": "Ends the session with failure and a message describing why the session failed. This should be called when all feasible actions have been tried and the user's goal has not been achieved.",
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
        "name": "vision_api_ocr_print_out_all_text",
        "description": "Returns just all of the raw text in a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "vision_api_ocr_print_out_all_text_specific_location_bounding_boxes",
        "description": "Returns all of the raw text along with its associated bounding boxes in a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {},
    },
    {
        "name": "vision_api_ocr_find_text_specific_location_bounding_boxes",
        "description": "Given a string, find an instance of that printed text along with its associated bounding box in a new image taken with the robot's camera in the direction that the camera is currently facing.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to find in the image.",
                }
            },
        },
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
        "name": "vision_api_image_analysis_specific_object_bounding_boxes",
        "description": "Returns the bounding boxes for specific objects in a new image taken with the robot's camera in the direction that the camera is currently facing.",
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
            "content": 'You are controlling a helpful and benevolent robot to serve human requests to the best of your ability in the most effective and efficient manner possible. The initial requests will not follow any strict template and may be extremely varied. They will be provided in natural speech. The information provided to you will be a list of messages which will detail what has happened so far in the session. You will have to keep track of a "Goal" (what the human currently wants to be accomplished). You will be given a list of "Functions" (all of the possible actions the robot can take and the list of actions you can choose from). You are to always choose the most appropriate action from the list of "Functions" informed by the current context and what has happened in the past in the message history. The "Goal" may be changed by feedback from the human user only. This process will consist mostly of a feedback loop between you, the robot\'s hardware feedback, AI Computer Vision API function calls, and human user input. When interpreting the results from the AI Computer Vision API, know that the results may be slightly incomplete or certain words may be misspelled or missing. You will have to problem solve and try to use real-world logic to achieve a success state. Only in the case that all feasible actions have been tried and the user\'s goal has not been achieved should you end the session with failure. Here is an example situation: '
            + "role: user: I am thirsty. I want to drink something.\n"
            + "role: assistant: What kind of drink would you like?\n"
            + "role: user: Something healthy. I'm on a diet\n"
            + "role: assistant: content: null func_call: vision_api_image_analysis_generic_caption\n"
            + "role: function: name: vision_api_image_analysis_generic_caption content: recycle bin and trash can\n"
            + "role: assistant: content: null func_call: rotate_robot_camera parameters: degrees: 180\n"
            + "role: function: name: vision_api_image_analysis_generic_caption content: several cans of soda on a table\n"
            + "role: assistant: content: null func_call: vision_api_image_analysis_dense_caption\n"
            + "role: function: name: vision_api_image_analysis_dense_caption content: yellow can\na red can of soda\nwhite and blue container\ngreen soda can\n"
            + "role: assistant: content: null func_call: vision_api_ocr_print_out_all_text\n"
            + "role: function: name: vision_api_ocr_print_out_all_text content: Lemonade\n"
            + "role: assistant: content: null func_call: zoom_in\n"
            + "role: function: name: zoom_in content: null\n"
            + "role: assistant: content: null func_call: vision_api_ocr_print_out_all_text\n"
            + "role: function: name: vision_api_ocr_print_out_all_text content: Lemonade Nutrition Facts Serving Size 1 Calories 5 Sodium Coca-Cola Nutrition Facts Serving Calories 140 Total Fat Vita Coco 330 mL Nutrition Facts Calories 60 %Daily Value Sprite Caffeine free Nutrition Facts Calories 120\n"
            + "role: assistant: content: null func_call: vision_api_ocr_find_text_specific_location_bounding_boxes parameters: text: Lemonade\n"
            + "role: function: name: vision_api_ocr_find_text_specific_location_bounding_boxes content: Rectangle(x=830, y=530, w=400, h=230)\n"
            + "role: assistant: content: null func_call: rotate_robot_camera parameters: x: 830 y: 530 w: 400 h: 230\n"
            + "role: function: name: rotate_robot_camera content: null\n"
            + "role: assistant: content: null func_call: point_at_object\n"
            + "role: function: name: point_at_object content: null\n"
            + "role: assistant: content: null func_call: send_picture_to_user\n"
            + "role: function: name: send_picture_to_user content: null\n"
            + "role: assistant: content: I found a can of lemonade that has 5 calories. Would you like this drink?\n"
            + "role: user: Yes, I would like that drink.\n"
            + "role: assistant: content: null func_call: end_session_with_success\n",
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

# - Vision API: OCR (Print out all text)
# - Vision API: OCR (Print out all text associated with specific location bounding boxes)
# - Vision API: Image Analysis (Generic caption)
# - Vision API: Image Analysis (Dense caption)
# - Vision API: Image Analysis (Specific location bounding boxes)
# - Vision API: Face
# - Vision API: Spatial Analysis

# - Speech API: Text to Speech

# Example:
# user: "I am thirsty. I want to drink something.
