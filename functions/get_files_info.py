import os
from google.genai import types

def get_files_info(working_directory, directory = "."):




    abs_path = os.path.abspath(working_directory)
    abs_working_path = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_working_path.startswith(abs_path):
        return f"Error: working file is outside the directory '{directory}'"

    contents = os.listdir(abs_working_path)
    final_response=""
    for content in contents:
        content_path = os.path.join(abs_working_path, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response+=f"Content: '{content}' \n Is present: '{is_dir}' \n Size: '{size}' \n"

    return final_response



schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description= "Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters= types.Schema(
        type = types.Type.OBJECT,
        properties={"directory":types.Schema(
            type=types.Type.STRING,
            description="Directory path to list files from, relative to the working directory (default is the working directory itself)"
        )}
    )
)