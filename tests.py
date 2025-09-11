from functions.get_files_info import get_files_info

print(f'Result for current directory: {get_files_info("calculator", ".")}')

'''
Result for current directory:
 - main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=92 bytes, is_dir=True 
 '''

print(f'Result for "pkg" directory: {get_files_info("calculator", "pkg")}')

'''
Result for 'pkg' directory:
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False
'''

print(f'Result for "/bin" directory: {get_files_info("calculator", "/bin")}')

'''
Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory
'''

print(f'Result for "../" directory: {get_files_info("calculator", "../")}')

'''
Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory
'''