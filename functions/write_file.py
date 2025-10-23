import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    
    absolute_path = os.path.realpath(working_directory)
    intended_path = os.path.join(absolute_path, file_path)
    true_path = os.path.realpath(intended_path)
    
    if not true_path.startswith(absolute_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        os.makedirs(os.path.dirname(true_path), exist_ok=True)
    except Exception as error:
        return f'Error: {error}'
        
    with open(true_path, "w") as file:
        try:
            file.write(content)
        except Exception as error:
            return f'Error: {error}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the specified file in the file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of the file to write content to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            )
        },
    ),
)