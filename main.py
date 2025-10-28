import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = sys.argv[1:]

    if "--verbose" in args:
        args.remove("--verbose")
        flag = "--verbose"
    else:
        flag = None

    user_prompt = " ".join(args)

    if not args:
        print("Invalid prompt detected!")
        print("Exiting")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    generate_content(client, messages, user_prompt, flag)

def generate_content(client, messages, user_prompt, flag):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if not response.function_calls:
            if flag == '--verbose':
                print(response.text)    
            return response.text
    
    for function_call in response.function_calls:
        result_content = call_function(function_call, verbose=(flag == '--verbose'))
        if not result_content.parts or not getattr(result_content.parts[0], 'function_response', None):
            raise RuntimeError('Missing function response from call_function')
        resp = result_content.parts[0].function_response.response
        if flag == "--verbose":
            print(f"-> {resp}")
        
functions_dict = {
    'get_file_content': get_file_content,
    'get_files_info': get_files_info,
    'run_python_file': run_python_file,
    'write_file': write_file
}

def call_function(function_call_part, verbose = False):
    function_call_part.args['working_directory'] = './calculator'
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    kwargs = dict(function_call_part.args)
    fn = functions_dict.get(function_name)

    if fn == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        function_result = fn(**kwargs)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )


if __name__ == "__main__":
    main()