from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import AzureChatOpenAI
import os
llm = AzureChatOpenAI(deployment_name="gpt-35-turbo-16k", openai_api_base=os.getenv("OPENAI_API_BASE"), openai_api_key=os.getenv("OPENAI_API_KEY"), openai_api_version="2023-05-15", openai_api_type="azure")

from langchain.tools import Tool, tool
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import AzureOpenAI

# tools = load_tools(["llm-math"], llm=llm)
# agent.run("What 20 raised to the 2 power?")
swagger_file_path="Vision\VisionAPISwagger.json"
@tool
def extract_api_descriptions(swagger_file_path: str):
    """
    You can safely ignore the swagger_file_path, if you need to call this function, just pass in the "Vision\VisionAPISwagger.json"
    This function gets a list of existing Azure Computer Vision API paths and descriptions
    It returns the "HTTP method/endpoint" as its key, and the description of this API as its value
    """
    import json
    descriptions = {}

    try:
        # Load the Swagger JSON file into a Python dictionary
        with open(swagger_file_path, 'r', encoding="utf-8") as f:
            swagger_data = json.load(f)

        # Check if the Swagger data contains the 'paths' field
        if 'paths' not in swagger_data:
            print("The Swagger file doesn't contain the 'paths' field.")
            return

        # Loop through each path and its methods to extract descriptions
        for path, methods in swagger_data['paths'].items():
            for method, details in methods.items():
                endpoint = f"{method.upper()} {path}"
                description = details.get('description', 'No description available')
                descriptions[endpoint] = description
    except Exception as e:
        print(f"An error occurred: {e}")

    return descriptions

tools = [extract_api_descriptions]


agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("What are the APIs details in the azure computer vision api")

# description = extract_api_descriptions("Vision\VisionAPISwagger.json")
# print(description)

# def get_endpoint_details(query: str) -> str:
#     """ This function takes the API name and method as input and returns the corresponding API details, including parameters, request headers, and a summary. 
#     These details can be further utilized to construct the correct parameters, headers, and body required to call the endpoint accurately.
#     This function should only be invoked when specific endpoint information is needed. The expected format for the input is "<path>,<method>".

#     Inputs:
#         1. "/xyz,post"
#         2. "/askdjhad,get"
#     """
#     import json
#     try:
#         vals = query.split(",")
#         resp = json.load(open(os.path.join(os.path.dirname(current_path), "swagger.json")))
#         for item in resp["paths"]:
#             for method, val in resp["paths"][item].items():
#                 if method == vals[1].strip() and vals[0].strip() == item:
#                     val.pop("description", None)
#                     val.pop("responses", None)
#                     val["name"] = vals[0].strip()
#                     val["method"] = vals[1].strip()
#                     return json.dumps(val)
                
#         resp = json.load(open(os.path.join(os.path.dirname(current_path), "swagger_cv.json")))
#         for item in resp["paths"]:
#             for method, val in resp["paths"][item].items():
#                 if method == vals[1].strip() and vals[0].strip() == item:
#                     val.pop("description", None)
#                     val.pop("responses", None)
#                     return json.dumps(val)
#         return f"\n\nThe input is invalid. It is likely that you have called the wrong tool or provided an input in the wrong format. The accepted format is: <path>,<method>."
#     except Exception as e:
#         return f"\nException: {e} \n The input is invalid. It is likely that you have called the wrong tool or provided an input in the wrong format. The accepted format is: <path>,<method>."
