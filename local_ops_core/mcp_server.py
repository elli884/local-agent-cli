import json
import sys
import logging
from secure_file_reader import safe_read_file

# creating a logging file 'audit_security.log' to log all the file access attempts by the AI
logging.basicConfig(
    filename='audit_security.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [MCP_FILE_SYSTEM] - %(message)s'
)

def mcp_list_tools():
    # Defines the tool according to the official MCP standard
    return {
        "tools": [
            {
                "name": "read_local_file",
                "description": "Reads the content of a local file in the workspace.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Relative path to the file"}
                    },
                    "required": ["file_path"]
                }
            }
        ]
    }

def execute_mcp_tool(tool_name: str, arguments: dict) -> str:
    if tool_name == "read_local_file":
        file_path = arguments.get("file_path")
        logging.info(f"AI is attempting to read file: {file_path}")
        try:
            content = safe_read_file(file_path)
            logging.info(f"Access GRANTED for file: {file_path}")
            return content
        except PermissionError as e:
            logging.warning(f"ACCESS DENIED: {str(e)}")
            return str(e)
    return "Tool not found."

if __name__ == "__main__":
    # MCP communicates by default via stdin/stdout using JSON-RPC
    # raw_input = sys.stdin.read()
    # if not raw_input:
    #     sys.exit(0)
        
    # try:
    #     request = json.loads(raw_input)
    #     if request.get("method") == "tools/list":
    #         print(json.dumps({"jsonrpc": "2.0", "result": mcp_list_tools(), "id": request.get("id")}))
    # except Exception as e:
    #     print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": None}))


    # Simulated MCP tool call from the AI
    result = execute_mcp_tool("read_local_file", {"file_path": "safe.txt"})
    print("Result for AI:", result)

    result_attack = execute_mcp_tool("read_local_file", {"file_path": "../../../../etc/passwd"})
    print("Result for AI (Attack Attempt):", result_attack)
