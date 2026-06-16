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

from app.services.chat_memory import (
    add_message
)

from app.services.query_rewrite import (
    rewrite_question
)

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_document(
    request: QueryRequest
):

    # ===================================
    # Rewrite Follow-up Question
    # ===================================

    rewritten_question = rewrite_question(
        request.question
    )

    print("=" * 50)
    print("Original:", request.question)
    print("Rewritten:", rewritten_question)
    print("=" * 50)

    # ===================================
    # Generate Query Embedding
    # ===================================

    query_embedding = generate_query_embedding(
        rewritten_question
    )

    # ===================================
    # Dense Retrieval
    # ===================================

    results = search_similar_chunks(
        query_embedding,
        limit=10
    )

    # ===================================
    # BM25 Retrieval
    # ===================================

    all_chunks = get_chunks()

    bm25_results = bm25_search(
        rewritten_question,
        all_chunks,
        top_k=5
    )

    # ===================================
    # Dense Chunks
    # ===================================

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

    # ===================================
    # BM25 Chunks
    # ===================================

    bm25_chunks = []

    for chunk, score in bm25_results:

        bm25_chunks.append(
            chunk
        )

    # ===================================
    # Hybrid Search Merge
    # ===================================

    hybrid_chunks = list(
        set(
            dense_chunks +
            bm25_chunks
        )
    )

    # ===================================
    # Reranking
    # ===================================

    ranked_chunks = rerank_chunks(
        rewritten_question,
        hybrid_chunks
    )

    # ===================================
    # Confidence Calculation
    # ===================================

    scores = [
        float(score)
        for _, score in ranked_chunks[:5]
    ]

    confidence = calculate_confidence(
        scores
    )

    # ===================================
    # Hallucination Guard
    # ===================================

    if confidence < 0.05:

        return {
            "question": request.question,
            "rewritten_question": rewritten_question,
            "confidence": confidence,
            "answer": "Insufficient evidence found."
        }

    # ===================================
    # Build Context
    # ===================================

    context = ""

    for chunk, score in ranked_chunks[:5]:

        context += chunk
        context += "\n\n"

    # ===================================
    # Context Chunks For UI
    # ===================================

    context_chunks = []

    for chunk, score in ranked_chunks[:5]:

        context_chunks.append({
            "text": chunk,
            "rerank_score": float(score)
        })

    # ===================================
    # Save User Message
    # ===================================

    add_message(
        "user",
        request.question
    )

    # ===================================
    # Generate Final Answer
    # ===================================

    answer = generate_answer(
        rewritten_question,
        context
    )

    # ===================================
    # Save Assistant Message
    # ===================================

    add_message(
        "assistant",
        answer
    )

    # ===================================
    # Response
    # ===================================

    return {

        "question": request.question,

        "rewritten_question": rewritten_question,

        "answer": answer,

        "confidence": confidence,

        "retrieved_dense": len(
            dense_chunks
        ),

        "retrieved_bm25": len(
            bm25_chunks
        ),

        "retrieved_hybrid": len(
            hybrid_chunks
        ),

        "sources": sources,

        "context_chunks": context_chunks
    }