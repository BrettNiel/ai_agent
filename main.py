import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

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
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
    )

    if flag == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Response: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print (f"Response: {response.text}")
        

if __name__ == "__main__":
    main()