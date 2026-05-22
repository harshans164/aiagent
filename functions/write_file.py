import os 
from google.genai import types

def write_file(working_directory, file_path, content):

    working_directory_abs = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory_abs, target_path]) != working_directory_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    if not os.path.exists(working_directory_abs):
        os.makedirs(working_directory_abs, exist_ok=True)


    try:
        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Failed to write in '{file_path}'"
    

scheme_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes plain text content to a specified file within the allowed working directory. Use this tool whenever you need to create a new file or overwrite an existing file with updated text code, scripts, documentation, or data.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path or filename where the content should be saved (e.g., 'src/main.py' or 'README.md'). It must stay within the permitted working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The exact plain text or code string to be written into the file. Existing content in the file will be overwritten."
            )
        },

    )
)