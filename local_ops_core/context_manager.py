import ollama
import os
from dotenv import load_dotenv

load_dotenv()


def generate_with_strict_system_prompt(system_instruction: str, user_query: str):
    # SLMs need a crystal-clear separation of roles to avoid hallucinating
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]
    
    try:
        response = ollama.chat(
            model=os.getenv("OLLAMA_PHI", "phi3:latest"), # Phi-3 is extremely strong with strict system prompts
            messages=messages,
            options={"temperature": 0.0} # Constant, deterministic answers
        )
        return response['message']['content']
    except Exception as e:
        return f"Generation error: {str(e)}"

if __name__ == "__main__":
    sys_instruction = "You are a precise compiler assistant. Respond ONLY with valid Python code. No Markdown, no text."
    query = "Write a function that reverses a list."
    print(generate_with_strict_system_prompt(sys_instruction, query))