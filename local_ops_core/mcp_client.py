import ollama
import json
import os 
from dotenv import load_dotenv

load_dotenv()

def ask_ollama_with_mcp_tools(user_prompt: str):
    # Pass the tools provided via MCP to the model
    from mcp_server import mcp_list_tools
    available_tools = mcp_list_tools()["tools"]
    
    system_instruction = (
        f"You have access to local tools. If the user wants to read a file, "
        f"respond in JSON format with the tool call. Available tools: {json.dumps(available_tools)}"
    )
    
    response = ollama.chat(
        model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        options={"temperature": 0.0}
    )
    return response['message']['content']

if __name__ == "__main__":
    query = "Can you check what is written in the file 'config.txt'?"
    tool_decision = ask_ollama_with_mcp_tools(query)
    print(f"Decision of the local AI:\n{tool_decision}")