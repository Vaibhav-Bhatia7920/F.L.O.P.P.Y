import json
from openai import OpenAI
from tools import list_files, read_file, search_files, summarize_file

# 🔑 Init client
client = OpenAI()

# 🛠️ TOOL SCHEMAS
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in the current directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string"}
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
                    "filename": {"type": "string"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for a string across files",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string"},
                    "query": {"type": "string"}
                },
                "required": ["directory", "query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_file",
            "description": "Summarize a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        }
    }
]

# 🧠 TOOL MAP
TOOL_MAP = {
    "list_files": list_files,
    "read_file": read_file,
    "search_files": search_files,
    "summarize_file": summarize_file
}

# 📡 GPT CALL (TOOLS PASSED HERE ✅)
def chat(messages, tools):
    return client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

# 🔁 AGENT LOOP
def agent_loop(user_input):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI agent.\n"
                "Use tools step-by-step.\n"
                "Do NOT repeat the same tool unnecessarily.\n"
            )
        },
        {"role": "user", "content": user_input}
    ]

    for i in range(10):
        print(f"\n--- Loop iteration {i+1} ---")

        response = chat(messages, tools)  # ✅ TOOLS PASSED HERE
        msg = response.choices[0].message

        print("RAW RESPONSE:", msg)

        # ✅ TOOL CALL
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]

            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            print(f"Calling tool: {tool_name} with {tool_args}")

            if tool_name not in TOOL_MAP:
                return f"Unknown tool: {tool_name}"

            try:
                tool_output = TOOL_MAP[tool_name](**tool_args)
            except Exception as e:
                tool_output = f"Tool execution error: {str(e)}"

            # 🔥 Append assistant tool call
            messages.append({
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(tool_args)
                        }
                    }
                ]
            })

            # 🔥 Append tool response (CRITICAL)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_output)
            })

        else:
            # ✅ FINAL ANSWER
            final_text = msg.content if msg.content else ""

            messages.append({
                "role": "assistant",
                "content": final_text
            })

            return final_text

    return "❌ Failed after 10 iterations"


# ▶️ RUN
if __name__ == "__main__":
    user_input = input("Enter your question: ")
    answer = agent_loop(user_input)
    print("\nFinal Answer:\n", answer)