import os
from dotenv import load_dotenv
import argparse

from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import scheme_write_file

from functions.call_function import call_function

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Generate answer with Gemini API")
    parser.add_argument("prompt", type = str, help = "Help User")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]


    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    If the question is something which is not something related to coding tasks, just tell once "I am assigned to only coding tasks"
    """

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, scheme_write_file, schema_get_file_content, schema_run_python_file],
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    result=""
    max_iterations = 5
    for iter in range(max_iterations):
    
        response = client.models.generate_content(
            model='gemini-2.5-flash' , 
            contents=messages ,
            config=config,
        )

        if response.function_calls is None:
            print(response.text)
        else:
            for fnc_call in response.function_calls:
                print(f"Calling function: {fnc_call.name}({fnc_call.args})")




        print(response.text)
        print("")
        if args.verbose:
            print("STATS:")
            print(response.usage_metadata.prompt_token_count)
            print(response.usage_metadata.candidates_token_count)

#this loop basically adds context in the message it does not do any function call
        if response.candidates:
            for fnc in response.candidates:
                if fnc is None or fnc.content is None:
                    continue
                messages.append(result)


#this loop does the function call which the model instructs to do 
        if response.function_calls:
            for fnc in response.function_calls:
                result = call_function(fnc, args.verbose)
                messages.append(result)



        else:
            print(response.text)

  

if __name__ == "__main__":
    main()

