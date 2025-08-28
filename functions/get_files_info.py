import os

def get_files_info(working_directory, directory="."):
    
    absolute_path = os.path.join(working_directory, directory)
    
    if working_directory not in absolute_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if directory not in working_directory:
        return f'Error: "{directory}" is not a directory'

    for document in directory:
        print(f'- {os.path.basename(document)}: file_size={os.path.getsize(document)} bytes, is_dir={os.path.isdir(document)}')