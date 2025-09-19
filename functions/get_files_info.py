import os

def get_files_info(working_directory, directory="."):
    
    absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.abspath(os.path.join(working_directory, directory))

    if target_directory.startswith(absolute_path) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isdir(directory) == False:
        return f'Error: "{directory}" is not a directory'
    
    for file in directory:
        try:
            return f'- {os.path.basename(file)}: {os.path.getsize(file)} bytes, is_dir={os.path.isdir(file)}'
        except Exception as error:
            return f'Error: {error}'