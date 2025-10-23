import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

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

    if flag == "--verbose":
        print(f"User prompt: {user_prompt}")
        if not response.function_calls:
            print(f"Response: {response.text or ''}")
        for item in response.function_calls:
            print(f"Calling function: {item.name}({item.args})")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        if not response.function_calls:
            print (f"Response: {response.text or ''}")
        for item in response.function_calls:
            print(f"Calling function: {item.name}({item.args})")
        

if __name__ == "__main__":
    main()