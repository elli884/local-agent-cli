import argparse
import json
from mcp_client import ask_ollama_with_mcp_tools
from mcp_server import execute_mcp_tool

def main():
    parser = argparse.ArgumentParser(description="LocalOps v3.0 - Secure MCP File Engine")
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Query for the AI regarding local files"
    )

    args = parser.parse_args()

    print("⚡ Analyzing request via MCP client...")
    raw_decision = ask_ollama_with_mcp_tools(args.query)
    try:
        # Attempt to parse the model's JSON decision
        decision_json = json.loads(raw_decision)

        if "file_path" in decision_json:
            print("🎯 AI identified the need for a tool. Calling the MCP server tool...")
            result = execute_mcp_tool(
                "read_local_file",
                {"file_path": decision_json["file_path"]}
            )
            print(f"\n[MCP SYSTEM RESPONSE]:\n{result}")
        else:
            print(f"AI response: {raw_decision}")

    except json.JSONDecodeError:
        # The model returned plain text instead of JSON
        print(f"AI response (no tool required): {raw_decision}")


if __name__ == "__main__":
    main()

# Run from the terminal:
# uv run local_ops_core/app_v3.py --query "Read the contents of safe.txt"