import requests

def query_llm(prompt):
    params = {"model" : "llama3.1:latest" , "prompt" : prompt, "stream" : False}
    response = requests.post("http://localhost:11434/api/generate", json=params)
    return response.text

def construct_prompt(user_input , context):
    prompt = f"""
    Context: {context}
    
    You are a helpful assistant. Answer the following question with context provided. If you don't know the answer, say you don't know.:
    {user_input}
    """
    return prompt

def chat(messages, tools):

    system_prompt = f"""You are an AI agent. 
    You MUST use the provided tools to answer questions about files. 
    Do NOT respond with empty content. 
    If a tool is available, ALWAYS call it."""

    formatted_messages = [
        {"role": "system", "content": system_prompt}
    ] + messages

    params = {
        "model": "llama3.1:latest",
        "messages": formatted_messages,
        "tools": tools,
        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/chat",
        json=params
    )

    return response.json()

if __name__ == "__main__":
    pass
    
    