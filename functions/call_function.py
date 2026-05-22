from google.genai import types

from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python_file import run_python_file
from .write_file import write_file

from config import WORKING_DIRECTORY



def call_function(
        function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    
    else:
        print(f" - Calling function: {function_call.name}")


    if function_call.name == "get_files_info":
        result = get_files_info(WORKING_DIRECTORY, **function_call.args)
    if function_call.name == "get_file_content":
        result = get_file_content(WORKING_DIRECTORY, **function_call.args)
    if function_call.name == "run_python_file":
        result = run_python_file(WORKING_DIRECTORY, **function_call.args)
    if function_call.name == "write_file":
        result = write_file(WORKING_DIRECTORY, **function_call.args)
    if function_call.name == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": result},
            )
        ],
    )

        


