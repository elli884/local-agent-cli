import json
import os
import sys
import os
import ast
from pathlib import Path
from secure_file_reader import ALLOWED_WORKSPACE

def mcp_write_tool_definition():
    return {
        "name": "write_local_file",
        "description": "Creates a NEW file inside the workspace with the specified content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative destination path"
                },
                "content": {
                    "type": "string",
                    "description": "The complete text/code content of the file"
                }
            },
            "required": ["file_path", "content"]
        }
    }

def execute_write(file_path: str, content: str) -> str:
    # Absolute path validation against path traversal
    target_path = Path(os.path.join(ALLOWED_WORKSPACE, file_path)).resolve()

    if not target_path.is_relative_to(ALLOWED_WORKSPACE):
        return "🚨 Security veto: Write access outside the workspace has been denied!"

    target_path.parent.mkdir(parents=True, exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Successfully written: {file_path}"

def validate_and_execute_write(file_path: str, content: str) -> str:
    # Check for Python syntax errors before writing
    if file_path.endswith(".py"):
        try:
            ast.parse(content)
        except SyntaxError as e:
            # The error is caught and the file is not written
            raise ValueError(
                f"Python syntax validation failed. Invalid Python code detected! "
                f"Line {e.lineno}: {e.msg}"
            )

    from mcp_writer_server import execute_write

    return execute_write(file_path, content)


if __name__ == "__main__":
    # Test run of the standalone write operation
    # print(execute_write("generated_code.py", "print('Hello from Local MCP AI')"))
    # print(execute_write("/wrong/malicious.py", "malicious content"))  # Should be blocked

    # Test run of invalid code (missing closing quote)
    broken_code = "print('This is a broken line of code"
    try:
        print(validate_and_execute_write("broken.py", broken_code))
    except ValueError as e:
        print(e)