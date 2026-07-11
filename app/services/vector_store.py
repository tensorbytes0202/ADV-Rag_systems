import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.core.settings import settings


# ==========================================================
# Qdrant Client
# ==========================================================

client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT
)

COLLECTION_NAME = settings.COLLECTION_NAME


# ==========================================================
# Create Collection
# ==========================================================

def create_collection():

    print("=" * 60)
    print("Connecting to Qdrant...")
    print("=" * 60)

    collections = client.get_collections()

    existing = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(

            collection_name=COLLECTION_NAME,

            vectors_config=VectorParams(

                size=settings.EMBEDDING_DIM,

                distance=Distance.COSINE

            )

        )

        print(f"Collection '{COLLECTION_NAME}' created.")

    else:

        print(f"Collection '{COLLECTION_NAME}' already exists.")


# ==========================================================
# Store Embeddings
# ==========================================================

def store_embeddings(

    chunks,

    embeddings,

    document_name

):

    if not chunks:

        print("No chunks found.")

        return

    if not embeddings:

        print("No embeddings found.")

        return

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(

            PointStruct(

                id=str(uuid.uuid4()),

                vector=embedding,

                payload={

                    "chunk_id": str(uuid.uuid4()),

                    "parent_id": chunk["parent_id"],

                    "child_id": chunk["child_id"],

                    "parent_text": chunk["parent_text"],

                    "text": chunk["text"],

                    "document_name": chunk["document"],

                    "page": chunk["page"]

                }

            )

        )

    batch_size = 100

    total_batches = (

        len(points) + batch_size - 1

    ) // batch_size

    print(f"Total Points : {len(points)}")
    print(f"Total Batches : {total_batches}")

    for i in range(

        0,

        len(points),

        batch_size

    ):

        batch = points[i:i + batch_size]

        print(

            f"Uploading Batch {(i // batch_size) + 1}/{total_batches}"

        )

        client.upsert(

            collection_name=COLLECTION_NAME,

            points=batch

        )

        print(

            f"Uploaded Batch {(i // batch_size) + 1}/{total_batches}"

        )

    print("Embedding Upload Complete")


# ==========================================================
# Dense Retrieval
# ==========================================================

def search_similar_chunks(

    query_embedding,

    limit=10,

    document_name=None,

    page=None

):

    conditions = []

    # --------------------------------------
    # Document Filter
    # --------------------------------------

    if document_name:

        conditions.append(

            FieldCondition(

                key="document_name",

                match=MatchValue(

                    value=document_name.strip()

                )

            )

        )

    # --------------------------------------
    # Page Filter
    # --------------------------------------

    if page is not None:

        conditions.append(

            FieldCondition(

                key="page",

                match=MatchValue(

                    value=page

                )

            )

        )

    query_filter = None

    if conditions:

        query_filter = Filter(

            must=conditions

        )

    print("=" * 60)
    print("SEARCH REQUEST")
    print("Document :", document_name)
    print("Page     :", page)
    print("Limit    :", limit)
    print("=" * 60)

    if query_filter:

        print("QUERY FILTER")
        print(query_filter)
        print("=" * 60)

    # --------------------------------------
    # Qdrant Search
    # --------------------------------------

    search_result = client.query_points(

        collection_name=COLLECTION_NAME,

        query=query_embedding,

        query_filter=query_filter,

        limit=limit

    )

    print("=" * 60)
    print("RESULTS FOUND :", len(search_result.points))
    print("=" * 60)

    if search_result.points:

        print("FIRST RESULT")

        print(search_result.points[0].payload)

        print("=" * 60)

    return search_result.points


# ==========================================================
# Debug Utility
# ==========================================================

def debug_search():

    result = client.query_points(

        collection_name=COLLECTION_NAME,

        query=[0.0] * settings.EMBEDDING_DIM,

        limit=1

    )

    print(result.points)