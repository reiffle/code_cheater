import os
import json
from dotenv import load_dotenv
from openai import OpenAI

import argparse
from prompts import system_prompt
from call_functions import available_functions

load_dotenv() #load .env variables into environment
api_key = os.environ.get("OPENROUTER_API_KEY") #get api key that was loaded into environment with load_dotenv()

if api_key is None:
    raise RuntimeError("no api key found")

def main():
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()
    # now we can access `args.user_prompt`
    messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
        #temperature=0, #helps to make output more uniform between ai responses
    )
    if response.usage==None:
        raise RuntimeError("unexpected error occurrred")
    message=response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        prompt=response.usage.prompt_tokens
        complete=response.usage.completion_tokens
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt}")
            print(f"Response tokens: {complete}")
        print("Response:")
        print(message.content)

if __name__ == "__main__":
    main()
