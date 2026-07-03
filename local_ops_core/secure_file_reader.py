from pathlib import Path
import os

ALLOWED_WORKSPACE = Path("./workspace").resolve()

def safe_read_file(relative_path: str) -> str:
    # Create the absolute path and normalize it (removes '../../')
    target_path = Path(os.path.join(ALLOWED_WORKSPACE, relative_path)).resolve()

    # Security guardrail: Is the target path still inside the allowed workspace?
    if not target_path.is_relative_to(ALLOWED_WORKSPACE):
        raise PermissionError(
            f"🚨 Security veto: Path traversal detected! Access denied for: {relative_path}"
        )

    if not target_path.exists():
        return "Error: File does not exist."

    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    # Create test workspace
    ALLOWED_WORKSPACE.mkdir(exist_ok=True)
    (ALLOWED_WORKSPACE / "safe.txt").write_text(
        "Confidential local project data.",
        encoding="utf-8"
    )

    # Test 1: Safe access
    try:
        print("Test 1 (Safe):", safe_read_file("safe.txt"))
    except Exception as e:
        print(e)

    # Test 2: Malicious attempt to access a file outside the workspace
    try:
        print("Test 2 (Attack):", safe_read_file("../../../../etc/passwd"))
    except Exception as e:
        print(e)