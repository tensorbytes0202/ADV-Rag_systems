import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

client = QdrantClient(
    host="127.0.0.1",
    port=6333
)

COLLECTION_NAME = "rag_documents"


# =====================================================
# CREATE COLLECTION
# =====================================================

def create_collection():

    print("Connecting Qdrant...")

    collections = client.get_collections()

    print("Connected Successfully")

    existing = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing:

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


# =====================================================
# STORE EMBEDDINGS
# =====================================================

def store_embeddings(
    chunks,
    embeddings,
    document_name
):

    if len(chunks) == 0:
        print("No chunks found")
        return

    if len(embeddings) == 0:
        print("No embeddings found")
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

            f"Uploading Batch {(i//batch_size)+1}/{total_batches}"

        )

        client.upsert(

            collection_name=COLLECTION_NAME,

            points=batch

        )

        print(

            f"Uploaded Batch {(i//batch_size)+1}/{total_batches}"

        )

    print("Embedding Upload Complete")


# =====================================================
# SEARCH
# =====================================================

def search_similar_chunks(

    query_embedding,

    limit=10,

    document_name=None,

    page=None

):

    query_filter = None

    conditions = []

    # ==========================================
    # Incoming Search Request
    # ==========================================

    print("=" * 60)
    print("SEARCH REQUEST")
    print("Document :", repr(document_name))
    print("Page     :", page)
    print("=" * 60)

    # ==========================================
    # Document Filter
    # ==========================================

    if document_name:

        document_name = document_name.strip()

        conditions.append(
            FieldCondition(
                key="document_name",
                match=MatchValue(
                    value=document_name
            )
        )
    )

    # ==========================================
    # Page Filter
    # ==========================================

    if page is not None:

        conditions.append(

            FieldCondition(

                key="page",

                match=MatchValue(

                    value=page

                )

            )

        )

    # ==========================================
    # Build Query Filter
    # ==========================================

    if len(conditions) > 0:

        query_filter = Filter(

            must=conditions

        )

    # ==========================================
    # Debug Query Filter
    # ==========================================

    print("=" * 60)
    print("QUERY FILTER")
    print(query_filter)
    print("=" * 60)

    # ==========================================
    # Qdrant Search
    # ==========================================

    search_result = client.query_points(

        collection_name=COLLECTION_NAME,

        query=query_embedding,

        

        limit=limit

    )   
    print("=" * 60)
    print("FILTER VALUE :", repr(document_name))

    if len(search_result.points):

        print("PAYLOAD VALUE :", repr(search_result.points[0].payload["document_name"]))

    print("=" * 60)

    # ==========================================
    # Debug Results
    # ==========================================

    print("=" * 60)
    print("RESULTS FOUND :", len(search_result.points))
    print("=" * 60)

    if len(search_result.points) > 0:

        print("FIRST PAYLOAD")

        print(search_result.points[0].payload)

        print("=" * 60)

    return search_result.points

def debug_search():

    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=[0.0] * 384,
        limit=1
    )

    print(result.points)