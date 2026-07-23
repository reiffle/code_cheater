import os
from dotenv import load_dotenv
import argparse

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("No API key found")

from openai import OpenAI

def main():
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    querry=args.user_prompt
    response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": querry,
        }
    ],
    )
    if response.usage==None:
        raise RuntimeError("Unexpected error occurrred")
    prompt=response.usage.prompt_tokens
    complete=response.usage.completion_tokens
    print(f"User prompt: {querry}")
    print(f"Prompt tokens: {prompt}")
    print(f"Response tokens: {complete}")
    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
