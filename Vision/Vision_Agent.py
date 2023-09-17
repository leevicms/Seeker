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

import json

# @tool
def read_swagger_file_to_string() -> str:
    """
    This function reads the swagger file in JSON format to a dictionary. Before you use other tools or call other functions to get detailed information of each API, you must call this function first.
    Moreover, you only need to call this function once, and you can reuse the returned dictionary, swagger_data, for other functions or tools.  The parameter for this function is always "Vision\VisionAPISwagger.json".
    """
    filename = swagger_file_path
    with open(filename, 'r') as file:
        swagger_data = json.load(file)
    return json.dumps(swagger_data)

@tool
def extract_endpoints_and_methods_string(swagger_data_str: str) -> str:
    """
    This function gets all the API endpoints and methods from the swagger data, a dictionary, and returns each API's endpoint and method as a key value pair in a dictionary.
    """

    swagger_data = json.loads(read_swagger_file_to_string())
    endpoints_methods = {}
    paths = swagger_data.get('paths', {})

    for path, methods in paths.items():
        endpoints_methods[path] = list(methods.keys())

    return json.dumps(endpoints_methods)


@tool
def extract_parameters_string(swagger_data_str: str) -> str:
    """
    This functions extracts each API's parameter you must pass into in order to call the API.
    """

    swagger_data = json.loads(read_swagger_file_to_string())
    endpoint_parameters = {}
    paths = swagger_data.get('paths', {})
    
    for path, methods in paths.items():
        for method, details in methods.items():
            params = details.get('parameters', [])
            extracted_params = []
            for param in params:
                param_name = param.get('name', 'Unnamed')
                param_type = param.get('in', 'Unknown')
                param_required = param.get('required', False)
                extracted_params.append({
                    'name': param_name,
                    'type': param_type,
                    'required': param_required
                })
            endpoint_key = f"{path}::{method.upper()}"
            endpoint_parameters[endpoint_key] = extracted_params
    
    return json.dumps(endpoint_parameters)

@tool
def extract_response_status_codes_string(swagger_data_str: str) -> str:
    """
    This function extracts each API's response and its status code. You can learn what to expect from calling each API.
    """

    swagger_data = json.loads(read_swagger_file_to_string())
    endpoint_responses = {}
    paths = swagger_data.get('paths', {})
    
    for path, methods in paths.items():
        for method, details in methods.items():
            responses = details.get('responses', {})
            status_codes = {}
            for status_code, response_details in responses.items():
                description = response_details.get('description', 'No description provided')
                status_codes[status_code] = description
            endpoint_key = f"{path}::{method.upper()}"
            endpoint_responses[endpoint_key] = status_codes
            
    return json.dumps(endpoint_responses)

@tool
def extract_request_body_schema_string(swagger_data_str: str) -> str:
    """
    This function gets each api's request body schema
    """

    swagger_data = json.loads(read_swagger_file_to_string())
    endpoint_request_body = {}
    paths = swagger_data.get('paths', {})
    
    for path, methods in paths.items():
        for method, details in methods.items():
            request_body = details.get('requestBody', {})
            schema = request_body.get('content', {}).get('application/json', {}).get('schema', {})
            endpoint_key = f"{path}::{method.upper()}"
            endpoint_request_body[endpoint_key] = schema
    
    return json.dumps(endpoint_request_body)

@tool
def search_product_info(product_name: str) -> str:
    """
    This function browse the web to search the information related to a product
    """

    return "The rela"

tools = [extract_endpoints_and_methods_string, extract_parameters_string, extract_response_status_codes_string, extract_request_body_schema_string]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("I want to find the lowest caloried drink in an image")
# swagger_data = read_swagger_file("random")
# endpoints = extract_endpoints_and_methods(swagger_data)
# parameters = extract_parameters(swagger_data)
# response_info = extract_response_status_codes(swagger_data)

# print("==============endpoints==============")
# print(endpoints)
# print("=============parameters==============")
# print(parameters)
# print("=============responseinfo============")
# print(response_info)

