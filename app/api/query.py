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

    # Retrieve Chunks from Qdrant
    results = search_similar_chunks(
        query_embedding,
        limit=10
    )

    retrieved_chunks = []
    sources = []

    for result in results:

        retrieved_chunks.append(
            result.payload.get(
                "text",
                ""
            )
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

    # Rerank Chunks
    ranked_chunks = rerank_chunks(
        request.question,
        retrieved_chunks
    )

    # Top Chunks Response
    response = []

    for chunk, score in ranked_chunks[:5]:

        response.append({
            "rerank_score": float(score),
            "text": chunk
        })

    # Confidence Score
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

    # Generate Final Answer
    answer = generate_answer(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }