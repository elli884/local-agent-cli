import numpy as np
from embedder import get_local_embedding

def cosine_similarity(v1: list, v2: list) -> float:
    """Calculates the mathmatical semilarity beetween two vectors (values [-1; 1])"""
    arr1 = np.array(v1)
    arr2 = np.array(v2)

    dot_product = np.dot(arr1, arr2)
    norm_a = np.linalg.norm(arr1)
    norm_b = np.linalg.norm(arr2)

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product /(norm_a*norm_b))

if __name__ == "__main__":
    # simulate test-database
    v_query = get_local_embedding("How is the weather?")
    v_doc1 = get_local_embedding("It's raining tomorrow in Berlin.")
    v_doc2 = get_local_embedding("Python is a programming language.")
    v_doc3 = get_local_embedding("What is the forecast like outside?")

    print(f"Similarity to weather-doc: {cosine_similarity(v_query, v_doc1):.4f}")
    print(f"Similarity to programming-doc: {cosine_similarity(v_query, v_doc2):.4f}")
    print(f"Similarity when using synonyms: {cosine_similarity(v_query, v_doc3):.4f}")
