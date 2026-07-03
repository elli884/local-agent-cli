import json
import sys

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

if __name__ == "__main__":
    # MCP communicates by default via stdin/stdout using JSON-RPC
    raw_input = sys.stdin.read()
    if not raw_input:
        sys.exit(0)
        
    try:
        request = json.loads(raw_input)
        if request.get("method") == "tools/list":
            print(json.dumps({"jsonrpc": "2.0", "result": mcp_list_tools(), "id": request.get("id")}))
    except Exception as e:
        print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": None}))

