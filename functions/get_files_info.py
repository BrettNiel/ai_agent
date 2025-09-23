import os

def get_files_info(working_directory, directory="."):
    
    absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not target_directory == absolute_path and not target_directory.startswith(absolute_path + os.sep):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    
    directory_list = []
    
    for file in os.listdir(target_directory):
        try:
            new_dir = os.path.join(target_directory, file)
            directory_list.append(f'- {file}: file_size={os.path.getsize(new_dir)} bytes, is_dir={os.path.isdir(new_dir)}')
        except Exception as error:
            return f'Error: {error}'
    
    return "\n".join(directory_list)