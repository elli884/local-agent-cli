import ollama
from embedder import get_local_embedding
from vector_store import cosine_similarity
from document_parser import chunk_text
import os
from dotenv import load_dotenv

load_dotenv()

# Our small "in-memory" database for testing
KNOWLEDGE_BASE = []

def add_to_knowledge_base(raw_text: str):
    chunks = chunk_text(raw_text)
    for chunk in chunks:
        embedding = get_local_embedding(chunk)
        KNOWLEDGE_BASE.append({"text": chunk, "embedding": embedding})

def query_rag(question: str) -> str:
    query_vector = get_local_embedding(question)
    
    # Calculate similarity for all fragments
    scored_chunks = []
    for item in KNOWLEDGE_BASE:
        score = cosine_similarity(query_vector, item["embedding"])
        scored_chunks.append((score, item["text"]))
        
    # Sort by highest similarity and take the top 2
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_chunks = scored_chunks[:2]
    
    # Assemble the context
    context = "\n---\n".join([text for score, text in top_chunks])
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Answer the user's question using ONLY the provided context. "
                "If the answer cannot be found in the context, reply exactly with 'I don't know'."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]

    response = ollama.chat(model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"), messages=messages)
    return response["message"]["content"]

if __name__ == "__main__":
    add_to_knowledge_base("The secret admin password for the local server is: HydroX42.")
    add_to_knowledge_base("The kitchen on the second floor is cleaned on Fridays at 2 PM.")
    
    print(query_rag("What is the admin password?"))