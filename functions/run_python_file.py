import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_directory_abs = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory_abs, target_path]) != working_directory_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_path]
    if args:
        command.extend(args)

    try:
        output = subprocess.run(command,
                                        text=True, 
                                        cwd = working_directory_abs, 
                                        timeout=30,
                                        capture_output=True)

        
        output_bits=[]
        if output.returncode!=0:
            output_bits.append("Process exited with code X")

        stderr_output = output.stderr.strip()
        stdout_output = output.stdout.strip()

        if not stderr_output and not stdout_output:
            output_bits.append("No output produced")
        else:
            if stdout_output:
                output_bits.append(stdout_output)
            if stderr_output:
                output_bits.append(stderr_output)

        return "\n".join(output_bits)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the permitted working directory. Use this tool whenever you need to test code you've written, run a script, or verify if an application executes successfully.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path or filename of the Python script to execute (e.g., 'main.py' or 'scripts/process_data.py'). Must end with a '.py' extension."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An optional list of string arguments to pass to the script on the command line (e.g., ['--verbose', 'input.csv'])."
            )
        },

    )
)