from sentence_transformers import SentenceTransformer
from app.core.settings import settings
model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)

def generate_embeddings(chunks):

    if not chunks:
        return []

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def generate_query_embedding(query):

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()