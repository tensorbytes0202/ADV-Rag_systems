import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "rag_documents"


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

        print(
            f"Collection '{COLLECTION_NAME}' created."
        )

    else:

        print(
            f"Collection '{COLLECTION_NAME}' already exists."
        )


def store_embeddings(
    chunks,
    embeddings,
    document_name
):

    if not chunks:
        print("No chunks found")
        return

    if not embeddings:
        print("No embeddings found")
        return

    points = []

    for idx, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        points.append(
            PointStruct(
                id=idx + 100000,
                vector=embedding,
                payload={
                    "chunk_id": str(
                        uuid.uuid4()
                    ),
                    "text": chunk,
                    "document_name": document_name
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(
        f"{len(points)} vectors stored successfully."
    )


def search_similar_chunks(
    query_embedding,
    limit=10
):

    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
    )

    return search_result.points