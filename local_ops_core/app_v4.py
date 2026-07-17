import argparse
import os
import sys
import json
import ollama
from dotenv import load_dotenv
from mcp_writer_server import validate_and_execute_write
from gatekeeper import human_in_the_loop_approval

load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="LocalOps v4.0 - Bounded Autonomy Write Engine"
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Code generation task"
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Target filename inside the workspace"
    )

    args = parser.parse_args()

    print(f"AI is generating code for {args.file}...")

    prompt = (
        f"Write only valid Python code for the following task: {args.task}. "
        "Respond ONLY with raw Python code. Do not include explanations, comments, or Markdown."
    )

    response = ollama.generate(
        model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
        prompt=prompt
    )
    proposed_code = response["response"].strip()

    # Validate syntax using the Python AST
    try:
        # Request Human-in-the-Loop approval
        if human_in_the_loop_approval(args.file, proposed_code):
            # Pass the approved code to the validated write process
            result = validate_and_execute_write(args.file, proposed_code)
            print(f"{result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()