
from app.services.metadata_parser import extract_metadata
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import (
    generate_query_embedding
)
from app.services.query_rewriter import (
    rewrite_query
)

from app.services.vector_store import (
    search_similar_chunks
)

from app.services.reranker_services import (
    rerank_chunks
)

from app.services.confidence_service import (
    calculate_confidence
)

from app.services.generation_service import (
    generate_answer
)

    # from app.services.bm_25_service import (
    #     bm25_search
    # )

from app.services.chat_memory import (
    add_message
)

from app.services.context_expansion import (
    expand_context
)
from app.services.context_compression import (
    compress_context
)

#from app.services.verification_service import (
 #   verify_answer
#)
from app.services.multi_query_service import (
    generate_queries
)
# from app.services.rrf_service import(
# rrf_fusion
# )
from app.services.query_classifier import (
    classify_query
)
from app.services.verification_service import (
    verify_answer
)



from app.services.query_router import get_retrieval_config
from app.services.document_registry import (
    get_active_document
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

    rewritten_question = rewrite_query(
    request.question
)
    metadata = extract_metadata(
    rewritten_question
        )
    print("=" * 50)
    print("FINAL DOCUMENT FILTER")
    print(metadata["document_name"])
    print("=" * 50)
        # ===================================
        # Active Document
        # ===================================

    import os

    if metadata["document_name"] is None:
            metadata["document_name"] = get_active_document()

    if metadata["document_name"]:
        metadata["document_name"] = os.path.basename(
            metadata["document_name"]
    ).strip()

    print("=" * 50)
    print("ACTIVE DOCUMENT")
    print(metadata["document_name"])
    print("=" * 50)
    print("=" * 50)
    print("METADATA")
    print(metadata)
    print("=" * 50)

    print("=" * 50)
    print("Original:", request.question)
    print("Rewritten:", rewritten_question)
    print("=" * 50)

    # ===================================
    # Multi Query Generation
    # ===================================

    queries = generate_queries(rewritten_question)

    if not queries:
        queries = [rewritten_question]

    queries = list(dict.fromkeys(queries))
    # ===================================
    # Adaptive Retrieval Config
    # ===================================

    query_type = classify_query(
        rewritten_question
)

    config = get_retrieval_config(
        query_type
)

    print("=" * 60)
    print("QUERY TYPE :", query_type)
    print("RETRIEVAL CONFIG :", config)
    print("=" * 60)
    # ===================================
    # Embedding
    # ===================================

    all_results = []

    for query in queries:

        

        print("=" * 60)
        print("MULTI QUERY")
        for q in queries:
            print(q)
            print("=" * 60)
        query_embedding = generate_query_embedding(query)
    
        print("=" * 50)
        print("Searching With Metadata")
        print("Document :", metadata["document_name"])
        print("Page :", metadata["page"])
        print("=" * 50)

        
        results = search_similar_chunks(

            query_embedding,

            limit=config["dense_top_k"],

            document_name=metadata["document_name"],

            page=metadata["page"]

)

        all_results.extend(results)

    unique_results = {}

    for result in all_results:

        chunk_id = result.payload.get("chunk_id")

        if chunk_id not in unique_results:

            unique_results[chunk_id] = result

        else:

            if result.score > unique_results[chunk_id].score:

                unique_results[chunk_id] = result

    results = list(unique_results.values())

    results.sort(
        key=lambda x: x.score,
        reverse=True
)

    print("=" * 60)
    print("TOTAL RETRIEVED :", len(all_results))
    print("UNIQUE CHUNKS   :", len(results))
    print("=" * 60)

    # ===================================
    # BM25 Retrieval
    # ===================================
    bm25_results = []

    # ===================================
# Parent Retrieval
# ===================================

    dense_chunks = []

    seen = set()

    for result in results:

        parent = result.payload.get("parent_text")

        if parent and parent not in seen:

            seen.add(parent)

            dense_chunks.append(parent)
    expanded_chunks = expand_context(
    results,
    window_size=config["window_size"]
)
    compressed_chunks = compress_context(

    rewritten_question,

    expanded_chunks,

    top_k=config["compression_top_k"]

)

    print("=" * 60)
    print("Compressed Chunks :", len(compressed_chunks))
    print("=" * 60)

    sources = []

    for result in results:

        payload = result.payload

        sources.append({

        "document": payload.get(
            "document_name",
            "Unknown"
        ),

        "page": payload.get(
            "page",
            "N/A"
        ),

        "chunk_id": payload.get(
            "chunk_id",
            "N/A"
        ),

        "parent_id": payload.get(
            "parent_id",
            "N/A"
        ),

        "vector_score": float(
            result.score
        )

    })

    print("=" * 50)
    print("Parent Chunks Retrieved :", len(dense_chunks))
    print("=" * 50)

    print("=" * 60)
    print("Parent Chunks :", len(dense_chunks))
    print("Expanded Chunks :", len(expanded_chunks))
    print("=" * 60)
    # ===================================
    # BM25 Chunks
    # ===================================

    bm25_chunks = []

    # ===================================
    # Hybrid Merge
    # ===================================

    hybrid_chunks = compressed_chunks

    # ===================================
    # RRF Debug
    # ===================================

    print("=" * 50)
    print(
    "RRF Chunks:",
    len(hybrid_chunks)
    )
    print("=" * 50)
    print("=" * 60)
    print("HYBRID CHUNKS")
    print(len(hybrid_chunks))

    for i, chunk in enumerate(hybrid_chunks[:5]):
        print(f"\nChunk {i}")
        print(type(chunk))
        print(chunk[:300] if chunk else chunk)

    print("=" * 60)

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

    confidence = calculate_confidence(scores) if scores else 0
    # ===================================
# Retrieval Failure
# ===================================

    if not ranked_chunks:

        return {

        "question": request.question,

        "rewritten_question": rewritten_question,

        "answer": "No relevant information found in the uploaded documents.",

        "verification": "FAILED",

        "confidence": 0,

        "retrieved_dense": 0,

        "retrieved_bm25": 0,

        "retrieved_hybrid": 0,

        "sources": [],

        "citations": [],

        "context_chunks": []

    }

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

    for idx, (chunk, score) in enumerate(
        ranked_chunks[:5]
):

        page = "N/A"
        document = "Unknown"

        if idx < len(sources):

            page = sources[idx].get(
            "page",
            "N/A"
        )

            document = sources[idx].get(
            "document",
            "Unknown"
        )

        context_chunks.append({

            "text": chunk,

            "rerank_score": float(score),

            "page": page,

            "document": document,

            "vector_score": (
                sources[idx]["vector_score"]
                if idx < len(sources)
                else 0
                        )
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
        context,
        query_type
    )

    # ===================================
    # Verification Layer
    # ===================================

    verification = verify_answer(
        rewritten_question,
         answer,
         context
     )
    print("=" * 60)
    print("VERIFICATION RESULT")
    print(verification)
    print("=" * 60)

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

    

    # ===================================
    # Citations
    # ===================================

    citations = []

    seen = set()

    for source in sources:

        key = (
            source["document"],
            source["page"]
    )

        if key in seen:
            continue

        seen.add(key)

        citations.append({

            "source_id": len(citations) + 1,

            "document": source["document"],

            "page": source["page"]

    })

        if len(citations) == 5:
            break

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

        "retrieved_parent": len(dense_chunks),

        "retrieved_expanded": len(expanded_chunks),

        "retrieved_compressed": len(compressed_chunks),
        "retrieved_dense": len(results),
    
        "retrieved_bm25": len(
            bm25_chunks
        ),

        "retrieved_hybrid": len(
            hybrid_chunks
        ),

        "sources": sources[:5],
        "citations": citations,

        "context_chunks": context_chunks
    }