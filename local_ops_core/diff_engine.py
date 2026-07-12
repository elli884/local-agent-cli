import difflib
from pathlib import Path
from secure_file_reader import ALLOWED_WORKSPACE


def generate_file_diff(file_path: str, new_content: str) -> str:
    target_path = Path(ALLOWED_WORKSPACE / file_path).resolve()

    if not target_path.exists():
        return f"--- NEW FILE: {file_path} ---\n{new_content}"

    with open(target_path, "r", encoding="utf-8") as f:
        old_content = f.read().splitlines()

    new_content_lines = new_content.splitlines()

    # Generate a standardized unified diff
    diff = difflib.unified_diff(
        old_content,
        new_content_lines,
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        lineterm="",
    )

    return "\n".join(diff)


if __name__ == "__main__":
    # Test run with a simulated diff
    print(
        generate_file_diff(
            "generated_code.py",
            "print('Hello from Local MCP AI')\n# New line added",
        )
    )