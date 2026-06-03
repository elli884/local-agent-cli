# This is an open-source project for bounded autonomy and local ai infrastructure

The project is my own challenge to improve ai-skills and implement a really helpful tool for using local modells. The project will have like 100 work packages which get developed step by step.

If you are intersted in the process and want to use the final result, hit the star-button to be up to date :)

# Day 1: Setup & Structured Validation — The Foundation of an AI Guardrail

## How to Get Ready

### 1. Install `uv`

Download and install `uv`:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify the installation:

```bash
uv --version
```

### 2. Install the Project Dependencies

Clone the repository and navigate to the project folder:

```bash
git clone <repository-url>
cd <project-folder>
```

Install all required dependencies:

```bash
uv sync
```

This command creates a virtual environment and installs every package specified in the project's lock file, ensuring you get the exact same setup used in this tutorial.

### 3. Run the Example

```bash
uv run guard.py
```

Now you are ready!
