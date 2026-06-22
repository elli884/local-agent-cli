import ollama
import time
import os 
from dotenv import load_dotenv

load_dotenv()

def route_and_execute(user_query: str):
    # Step 1: Check complexity extremely fast using a tiny model
    routing_prompt = f"Is the following request complex (requires deep thinking/code) or simple (fact/yes-no)? Answer ONLY with 'SIMPLE' or 'COMPLEX'. Request: {user_query}"
    
    t0 = time.time()
    route_response = ollama.generate(model=os.getenv("OLLAMA_QWEN", "qwen2.5:7b"), prompt=routing_prompt)
    decision = route_response['response'].strip().upper()
    
    print(f"Routing decision made by Qwen in {time.time()-t0:.2f}s: {decision}")
    
    # Step 2: Dynamic switch based on complexity
    if "SIMPLE" in decision or "SIMPEL" in decision: 
        print("Executing on resource-efficient model")
        final_response = ollama.generate(model=os.getenv("OLLAMA_QWEN", "qwen2.5:7b"), prompt=user_query)
    else:
        print("Task is complex.")
        final_response = ollama.generate(model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"), prompt=user_query)
        
    return final_response['response']

if __name__ == "__main__":
    print("-" * 40)
    print(route_and_execute("How much is 2 + 2?"))
    print("-" * 40)
    print(route_and_execute("Write a secure asynchronous web scraper in Python with error handling."))