import ollama

import os
from dotenv import load_dotenv

load_dotenv()

def get_local_embedding(text: str) -> list:
    """Translate text offline in a 768-dimensional vector"""
    response = ollama.embeddings(model=os.getenv("OLLAMA_EMBEDDING", "nomic-embed-text" ), prompt=text)
    return response["embedding"]

if __name__ == "__main__":
    vec = get_local_embedding("A tree is a plant")
    print(f"Vector successfully generated. Dimensions: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
