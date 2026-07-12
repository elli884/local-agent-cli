import sys
from diff_engine import generate_file_diff

def human_in_the_loop_approval(file_path: str, proposed_content: str) -> bool:
    # Show the operator the exact diff
    print("\n" + "-" * 50)
    print(f"MCP PROPOSAL FOR FILE: {file_path}")
    print("-" * 50)
    diff_output = generate_file_diff(file_path, proposed_content)
    print(diff_output)
    print("-" * 50)

    # Require explicit human interaction
    user_decision = input("Do you want to approve this change? (y/n): ").strip().lower()
    return user_decision == "y" or user_decision == "yes"


if __name__ == "__main__":
    approved = human_in_the_loop_approval("app.py", "print('Secure Code v2')")
    print(f"Approval status: {approved}")