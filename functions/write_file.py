import os

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