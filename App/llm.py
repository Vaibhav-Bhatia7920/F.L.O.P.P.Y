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
    STRICTLY call ONE tool at a time and wait for the response before calling another tool.
    You have accese to the tools so use them when needed. 
    ALWAYS check the tool_list provided, do not try to use your own tools.
    AFTER every iteration , check if users request has been completed.
    Do not answer questions if you don't have the information, instead use the tools to get the information you need to answer the question.
    See the result provided by the tool and use it to answer the question. If the tool provides an answer, use that answer in your next response.
    DO tool calling sequentially if multiple tools are provided.
    Think like this all the time - If the tool call provides an answer, use that answer in your next response.
    If the tool call provides an answer, use that answer in your next response.
    Tool calling sequentially means that if you have multiple tools to call, you should call the first tool with the user input, get the output, and then call the second tool with the output of the first tool, and so on.
    Chain the tools do not pass garbage arguments to the tools."""

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
    
    