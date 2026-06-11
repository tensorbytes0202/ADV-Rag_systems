from numpy import True_
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_embeddings(chunks):

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True_

    )

    return embeddings.tolist()