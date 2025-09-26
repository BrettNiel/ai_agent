import os

def write_file(working_directory, file_path, content):
    
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not file_path.startswith(absolute_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    