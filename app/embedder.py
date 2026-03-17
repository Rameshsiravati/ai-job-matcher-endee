from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str) -> list[float]:
    """Convert text to a 384-dimensional vector."""
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()