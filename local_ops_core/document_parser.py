
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    """Separates text into overlapping fragments for more precise retrieval."""
    chunks = []
    start = 0
    if len(text) <= chunk_size:
        return [text]
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # Move start back by chunk step size
        start += (chunk_size - overlap)

    return chunks

if __name__ == "__main__":
    sample = (
    "This is a pretty long text, which is simulating our documents. "
    "Shortly they will be chunked.\n"
    "In addition, the text gets separated\n"
    "so that the AI doesn't lose anything.\n"
    ) * 10

    fragments= chunk_text(sample, chunk_size=150, overlap=30)
    print(f"Number of chunks: {len(fragments)}")
    print(f"Chunk 1: {fragments[0]}")
    print(f"Chunk 2: {fragments[1]}")
