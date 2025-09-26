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
            new_file = file.read(MAX_CHARACTER_LIMIT + 1)
            if len(new_file) > MAX_CHARACTER_LIMIT:
                 file_content_string = new_file[:MAX_CHARACTER_LIMIT] + f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                  file_content_string = new_file
            return file_content_string           
    except Exception as error:
            return f'Error: {error}'