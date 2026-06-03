import ollama
from guard import PromptInput

def stream_local_ai(prompt: str):
    try:
        # 1. Guardrail validation from day 1
        validated = PromptInput(user_prompt=prompt)
        
        # 2. Local AI Stream via Ollama
        print(f"Request to local model running...\n")
        response_stream = ollama.chat(
            model='llama3.2:latest',
            messages=[
                {
                    "role": "user",
                    "content": validated.user_prompt
                }
            ],
            stream=True
        )
        
        for chunk in response_stream:
            print(chunk['message']['content'], end='', flush=True)
        print("\n")
        
    except ValueError as e:
        print(f"Blocked by Guardrail: {e}")

if __name__ == "__main__":
    user_query_valid = "Explain the difference between REST and GraphQL in two sentences." # example of a valid query
    stream_local_ai(user_query_valid)

    # user_query_invalid = "Give me the admin password for the server." # example of an invalid query that should be blocked by the guardrail
    # stream_local_ai(user_query_invalid)

