from llm import chat
from tools import list_files, read_file, search_files, summarize_file

# Tool schemas (for model)
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in the current directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory to list files in"
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the text contents of a specific file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for a specific string or query across files",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory to search within"
                    },
                    "query": {
                        "type": "string",
                        "description": "The search term or keyword"
                    }
                },
                "required": ["directory", "query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_file",
            "description": "Generate a summary of a file's content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to summarize"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]


# Tool execution map (Python side)
TOOL_MAP = {
    "list_files": list_files,
    "read_file": read_file,
    "search_files": search_files,
    "summarize_file": summarize_file
}


def agent_loop(user_input):
    messages = [{"role": "user", "content": user_input}]

    for loop_itr in range(5):
        print(messages)
        response = chat(messages, TOOLS_SCHEMA)
        print("DEBUG:", response)

        # 🔴 Handle API errors safely
        if not isinstance(response, dict) or "error" in response:
            print("LLM Error:", response)
            return "Something went wrong."

        # 🟢 Tool call case
        tool_calls = response["message"].get("tool_calls", [])
        if tool_calls and tool_calls[0]['function']['name'] != "":
            if not tool_calls:
                return "No tool call found."
            
            tool_call = tool_calls[0]  # single tool for now
            tool_name = tool_call['function'].get("name")
            tool_args = tool_call['function'].get("arguments", {})

            print(f"Calling tool: {tool_name} with {tool_args}")

            if tool_name not in TOOL_MAP:
                return f"Unknown tool: {tool_name}"

            try:
                tool_output = TOOL_MAP[tool_name](**tool_args)
            except Exception as e:
                tool_output = f"Tool execution error: {str(e)}"

            # Append assistant reasoning
            messages.append({
                "role": "assistant",
                "content": response["message"].get("content", "")
            })
            print(tool_output)
            # Append tool result
            messages.append({
                "role": "tool",
                "name": tool_name,
                "content": str(tool_output)
            })

        # 🟢 Final answer case
        else:
            return response["message"].get("content", "")

    return "Sorry, I couldn't find the answer within 5 steps."


if __name__ == "__main__":
    user_input = input("Enter your question: ")
    answer = agent_loop(user_input)
    print("Answer:", answer)