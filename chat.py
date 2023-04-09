import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_message(role, content):
    return {"role": role, "content": content}

def chat(system, message_history, model="gpt-3.5-turbo"):
    messages = []
    messages.append(create_message("system", system))

    for role, content in message_history[-5:]:
        messages.append(create_message(role, content))

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )

    return response['choices'][0]['message']['content']
