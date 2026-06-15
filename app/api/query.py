from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import (
    generate_query_embedding
)

from app.services.vector_store import (
    search_similar_chunks
)

from app.services.reranker_services import (
    rerank_chunks
)

from app.services.confidence_services import (
    calculate_confidence
)

from app.services.generation_service import (
    generate_answer
)

from app.services.bm_25_service import (
    bm25_search
)

from app.services.chunk_store import (
    get_chunks
)

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_document(
    request: QueryRequest
):

    # Generate Query Embedding
    query_embedding = generate_query_embedding(
        request.question
    )

    # Dense Retrieval
    results = search_similar_chunks(
        query_embedding,
        limit=10
    )

    # BM25 Retrieval
    all_chunks = get_chunks()

    bm25_results = bm25_search(
        request.question,
        all_chunks,
        top_k=5
    )

    # Dense Chunks
    dense_chunks = []

    sources = []

    for result in results:

        chunk_text = result.payload.get(
            "text",
            ""
        )

        dense_chunks.append(
            chunk_text
        )

        sources.append({
            "document": result.payload.get(
                "document_name",
                "Unknown"
            ),
            "chunk_id": result.payload.get(
                "chunk_id",
                "N/A"
            ),
            "vector_score": float(
                result.score
            )
        })

    # BM25 Chunks
    bm25_chunks = []

    for chunk, score in bm25_results:

        bm25_chunks.append(
            chunk
        )

    # Hybrid Merge
    hybrid_chunks = list(
        set(
            dense_chunks +
            bm25_chunks
        )
    )

    # Reranking
    ranked_chunks = rerank_chunks(
        request.question,
        hybrid_chunks
    )

    # Top Results
    response = []

    for chunk, score in ranked_chunks[:5]:

        response.append({
            "rerank_score": float(score),
            "text": chunk
        })

    # Confidence
    scores = [
        float(score)
        for _, score in ranked_chunks[:5]
    ]

    confidence = calculate_confidence(
        scores
    )

    # Hallucination Guard
    if confidence < 0.50:

        return {
            "question": request.question,
            "confidence": confidence,
            "answer": "Insufficient evidence found."
        }

    # Build Context
    context = ""

    for chunk, score in ranked_chunks[:5]:

        context += chunk
        context += "\n\n"

    # Generate Answer
    answer = generate_answer(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer,
        "confidence": confidence,

        # Debug Metrics
        "retrieved_dense": len(
            dense_chunks
        ),

        "retrieved_bm25": len(
            bm25_chunks
        ),

        "retrieved_hybrid": len(
            hybrid_chunks
        ),

        "sources": sources
    }