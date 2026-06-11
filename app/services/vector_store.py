from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

# =========================
# Qdrant Client
# =========================

client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "rag_documents"


# =========================
# Create Collection
# =========================

def create_collection():

    collections = client.get_collections()

    existing_collections = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing_collections:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print(f"Collection '{COLLECTION_NAME}' created.")

    else:

        print(f"Collection '{COLLECTION_NAME}' already exists.")


# =========================
# Store Embeddings
# =========================

def store_embeddings(
    chunks,
    embeddings
):

    points = []

    for idx, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "text": chunk
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"{len(points)} vectors stored successfully.")


# =========================
# Search Vectors
# =========================

def search_similar_chunks(
    query_embedding,
    limit=5
):

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit
    )

    return results