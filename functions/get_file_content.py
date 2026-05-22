import os
from config import MAX_STRING_LIMIT
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'


    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_STRING_LIMIT)
            if len(f.read())>MAX_STRING_LIMIT:
                file_content_string+=f'\n [...File "{file_path}" truncated at {MAX_STRING_LIMIT} characters]'

            return file_content_string

    except Exception as e:
        return f"Error reading the file '{file_path}'"
    


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and retrieves the text content of a specific file within the permitted working directory. Use this tool whenever you need to inspect code, view configuration files, read logs, or review documentation.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path or filename of the file to be read (e.g., 'src/utils.py' or 'config.json'). Must point to a file inside the allowed working directory."
            )
        },
    )
)