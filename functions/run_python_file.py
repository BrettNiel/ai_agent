import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    absolute_path = os.path.realpath(working_directory)
    intended_path = os.path.join(absolute_path, file_path)
    true_path = os.path.realpath(intended_path)

    if not true_path.startswith(absolute_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(true_path):
        return f'Error: File "{file_path}" not found.'
    
    if not true_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        edited_arguments = ['python', true_path] + args
        result = subprocess.run(edited_arguments, timeout=30, cwd=working_directory, capture_output=True, check=True)
        decoded_stdout = result.stdout.decode('utf-8')
        decoded_stderr = result.stderr.decode('utf-8')
        if decoded_stdout.strip() == '' and decoded_stderr.strip() == '':
            return f'No output produced'
        return f'STDOUT: {decoded_stdout}, \nSTDERR:{decoded_stderr}'
    except subprocess.CalledProcessError as error:
        return f'Process exited with code : {error.returncode}'
    except Exception as error:
        return f'Error: executing Python file: {error}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file located at the given file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to execute the Python file.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to execute for the given Python file.",
            ),
        },
    ),
)