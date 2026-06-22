from huggingface_hub.inference._generated.types import document_question_answering
from huggingface_hub.inference._generated.types import document_question_answering
from huggingface_hub.inference._generated.types import document_question_answering
from typing import List

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

from app.services.verification_service import (
    verify_answer
)
from app.services.multi_query_service import (
    generate_queries
)
from app.services.rrf_service import(
rrf_fusion
)
router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    documents: List[str] = []


@router.post("/query")
def query_document(
    request: QueryRequest
):

    # ===================================
    # Rewrite Question
    # ===================================

    rewritten_question = request.question

    print("=" * 50)
    print("Original:", request.question)
    print("Rewritten:", rewritten_question)
    print("=" * 50)

    # ===================================
    # Multi Query Generation
    # ===================================

    queries = [
    rewritten_question
]

    print("=" * 50)
    print("Generated Queries:")
    print(queries)
    print("=" * 50)
    # ===================================
    # Embedding
    # ===================================

    all_results = []

    for query in queries:

        query_embedding = (
        generate_query_embedding(
            query
        )
    )

    results = search_similar_chunks(
        query_embedding,
        limit=20
    )

    all_results.extend(
        results
    )

    unique_results = {}

    for result in all_results:

        chunk_id = result.payload.get(
        "chunk_id"
    )

    unique_results[
        chunk_id
    ] = result

    results = list(
    unique_results.values()
)

    # ===================================
    # BM25 Retrieval
    # ===================================

    all_chunks = get_chunks()

    bm25_results = bm25_search(
        rewritten_question,
        all_chunks,
        top_k=20
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
        chunk["text"]
    )

    # ===================================
    # Hybrid Merge
    # ===================================

    hybrid_chunks = rrf_fusion(
    dense_chunks,
    bm25_chunks
            )

    # ===================================
    # RRF Debug
    # ===================================

    print("=" * 50)
    print(
    "RRF Chunks:",
    len(hybrid_chunks)
    )
    print("=" * 50)

    # ===================================
    # Reranking
    # ===================================

    ranked_chunks = rerank_chunks(
        rewritten_question,
        hybrid_chunks
    )

    print("\nTOP CHUNKS\n")

    for i, (chunk, score) in enumerate(
    ranked_chunks[:5]
):
     print("=" * 50)
     print("Score:", score)
     print(chunk[:500])

    # ===================================
    # Confidence
    # ===================================

    scores = [
        float(score)
        for _, score in ranked_chunks[:5]
    ]

    confidence = calculate_confidence(
        scores
    )

    # ===================================
    # Retrieval Failure Check
    # ===================================

    # if confidence < 0.05:

    #     return {
    #         "question": request.question,
    #         "rewritten_question": rewritten_question,
    #         "confidence": confidence,
    #         "answer": "Insufficient evidence found."
    #     }

    print(
    "Confidence:",
    confidence
)

    # ===================================
    # Context Build
    # ===================================

    context = ""

    for chunk, score in ranked_chunks[:5]:

        context += chunk
        context += "\n\n"

    # ===================================
    # UI Chunks
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
    # Generate Answer
    # ===================================

    answer = generate_answer(
        rewritten_question,
        context
    )

    # ===================================
    # Verification Layer
    # ===================================

    # verification = verify_answer(
    #     rewritten_question,
    #     answer,
    #     context
    # )

    # if verification != "SUPPORTED":

    #     answer = (
    #         "Insufficient evidence found."
    #     )
    # ===================================
# Debug Answer
# ===================================

    print("\n" + "=" * 50)
    print("FINAL GENERATED ANSWER")
    print("=" * 50)
    print(answer)
    print("=" * 50 + "\n")

    verification = "DISABLED"

    # ===================================
    # Citations
    # ===================================

    citations = []

    for idx, source in enumerate(
        sources[:5]
    ):

        citations.append({
            "source_id": idx + 1,
            "document": source["document"]
        })

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

        "verification": verification,

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

        "citations": citations,

        "context_chunks": context_chunks
    }