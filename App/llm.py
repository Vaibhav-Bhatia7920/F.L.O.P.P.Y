import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = OpenAI()
# OPTIONAL (you can remove if not using Ollama)
def query_llm(prompt):
    params = {"model": "llama3.1:latest", "prompt": prompt, "stream": False}
    response = requests.post("http://localhost:11434/api/generate", json=params)
    return response.text


def construct_prompt(user_input, context):
    prompt = f"""
Context: {context}

You are a helpful assistant. Answer the following question with context provided.
If you don't know the answer, say you don't know.

Question:
{user_input}
"""
    return prompt


def chat(messages, tools):
    return client.chat.completions.create(
        model="gpt-5.4-mini",   # or gpt-5.4-nano
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )



if __name__ == "__main__":
    pass