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
if __name__ == "__main__":
    pass
    
    