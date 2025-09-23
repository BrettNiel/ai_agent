import os
from functions.config import MAX_CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(absolute_path + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, 'r') as file:
                file_content_string = file.read() 
                if len(file_content_string) > MAX_CHARACTER_LIMIT:
                    file_content_string = file_content_string[:MAX_CHARACTER_LIMIT] + f'[...File "{file_path}" truncated at 10000 characters]'
                    return file_content_string
                else:
                    return file_content_string
    except Exception as error:
            return f'Error: {error}'