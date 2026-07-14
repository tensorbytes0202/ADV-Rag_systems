from sentence_transformers import SentenceTransformer

from app.core.settings import settings

from app.services.embedding_cache import (
    get_embedding,
    set_embedding
)

# ==========================================================
# Load Model (only once)
# ==========================================================

model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)


# ==========================================================
# Document Embeddings
# ==========================================================

def generate_embeddings(chunks):

    if not chunks:
        return []

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )

    return embeddings.tolist()


# ==========================================================
# Query Embedding (with Redis Cache)
# ==========================================================

def generate_query_embedding(query: str):

    # Check Redis Cache
    cached = get_embedding(query)

    if cached is not None:

        return cached

    # Generate Embedding
    embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Save to Redis
    set_embedding(
        query,
        embedding
    )

    return embedding