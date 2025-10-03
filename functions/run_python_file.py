import os
import subprocess

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
        if result.stdout == None:
            return f'No output produced'
        return f'STDOUT: {result.stdout}, \nSTDERR:{result.stderr}'
    except subprocess.CalledProcessError as error:
        return f'Process exited with code : {error}'
    except Exception as error:
        return f'Error: executing Python file: {error}'