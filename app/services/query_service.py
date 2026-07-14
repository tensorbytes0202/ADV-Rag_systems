from app.services.retrieval_pipeline import (
    run_retrieval_pipeline,
    retrieve_chunks,
    build_context,
    build_sources,
    build_context_chunks,
    build_citations,
)

from app.services.response_builder import (
    build_success_response,
    build_failure_response
)

from app.services.reranker_services import rerank_chunks
from app.services.confidence_service import calculate_confidence
from app.services.generation_service import generate_answer
from app.services.followup_service import generate_followups
from app.services.verification_service import verify_answer
from app.services.chat_memory import add_message

from app.services.bm_25_service import bm25_search
from app.services.rrf_service import rrf_fusion
from app.services.performance_logger import PerformanceLogger
from app.services.cache_service import (
    get_cache,
    set_cache
)
from app.services.generation_service import (
    generate_answer,
    stream_answer
)

def process_query(question: str):


    logger = PerformanceLogger()
    
    # =====================================================
    # Response Cache
    # =====================================================

    cached_response = get_cache(question)

    if cached_response:

        print("=" * 60)
        print("RETURNING FROM REDIS CACHE")
        print("=" * 60)

        return cached_response
    
    
    logger.start("Pipeline")
    # =====================================================
    # Pipeline
    # =====================================================
    pipeline = run_retrieval_pipeline(question)
    print("=" * 60)
    print("QUERY DECOMPOSITION")
    print("=" * 60)

    for q in pipeline["subqueries"]:
        print("-", q)

    print("=" * 60)

    logger.stop("Pipeline")

    rewritten_question = pipeline["rewritten_question"]
    query_type = pipeline["query_type"]
    config = pipeline["config"]
    metadata = pipeline["metadata"]
    queries = pipeline["queries"]

    # =====================================================
    # Dense Retrieval
    # =====================================================
    print("Total Retrieval Queries :", len(queries))
    logger.start("Dense Retrieval")
    results = retrieve_chunks(
        queries,
        metadata,
        config
    )
    logger.stop("Dense Retrieval")
    if not results:

        return build_failure_response(
            question,
            rewritten_question
        )

    # =====================================================
    # Context
    # =====================================================

    context_data = build_context(
        question,
        results,
        config
    )

    parent_chunks = context_data["parent_chunks"]
    expanded_chunks = context_data["expanded_chunks"]
    compressed_chunks = context_data["compressed_chunks"]

    # =====================================================
    # Dense Sources
    # =====================================================

    sources = build_sources(results)

    dense_chunks = []

    for source in sources:

        dense_chunks.append({

            "text": source["text"],

            "page": source["page"],

            "document": source["document"],

            "chunk_id": source["chunk_id"],

            "parent_id": source["parent_id"],

            "vector_score": source["vector_score"],

            "retrieval_type": "dense"

        })

    # =====================================================
    # BM25 Retrieval
    # =====================================================
    logger.start("BM25")
    bm25_results = bm25_search(

        query=question,

        document_name=metadata["document_name"],

        top_k=config["bm25_top_k"]

    )
    logger.stop("BM25")

    bm25_chunks = []

    for chunk, score in bm25_results:

        chunk = dict(chunk)

        chunk["retrieval_type"] = "bm25"

        chunk["bm25_score"] = float(score)

        bm25_chunks.append(chunk)
        # =====================================================
    # Hybrid Retrieval (RRF)
    # =====================================================
    logger.start("RRF")
    hybrid_chunks = rrf_fusion(

        dense_chunks,

        bm25_chunks

    )
    logger.stop("RRF")
    print("=" * 60)
    print("Dense :", len(dense_chunks))
    print("BM25 :", len(bm25_chunks))
    print("Hybrid :", len(hybrid_chunks))
    print("=" * 60)

    # =====================================================
    # Reranking
    # =====================================================
    logger.start("Cross Encoder")
    ranked_chunks = rerank_chunks(

        question,

        hybrid_chunks

    )
    logger.stop("Cross Encoder")

    if not ranked_chunks:

        return build_failure_response(

            question,

            rewritten_question

        )

    # =====================================================
    # Confidence
    # =====================================================

    scores = [

        chunk["rerank_score"]

        for chunk in ranked_chunks[:5]

    ]

    confidence = calculate_confidence(

        scores

    )

    # =====================================================
    # Top Context (Generation + Verification)
    # =====================================================

    top_context = "\n\n".join(

        chunk["text"]

        for chunk in ranked_chunks[:5]

    )

    # =====================================================
    # Context for UI
    # =====================================================

    context_chunks = build_context_chunks(

        ranked_chunks

    )

    citations = build_citations(

        sources

    )

    # =====================================================
    # Chat Memory
    # =====================================================

    add_message(

        "user",

        question

    )
    
        # =====================================================
    # Generation
    # =====================================================
    logger.start("Generation")
    answer = generate_answer(

        question,

        top_context,

        query_type

    )
    logger.stop("Generation")

    # =====================================================
    # Follow-up Questions
    # =====================================================

    followups = generate_followups(

        question,

        answer

    )

    # =====================================================
    # Verification
    # =====================================================
    logger.start("Verification")
    verification = verify_answer(

        question,

        answer,

        top_context

    )
    logger.stop("Verification")

    print("=" * 60)
    print("VERIFICATION")
    print(verification)
    print("=" * 60)

    if not verification.get("supported", False):

        answer = (

            "⚠️ The generated answer could not be fully verified "

            "from the retrieved document."

        )

    # =====================================================
    # Save Assistant Message
    # =====================================================

    add_message(

        "assistant",

        answer

    )
    logger.print_summary()
    # =====================================================
    # Final Response
    # =====================================================

    logger.print_summary()

    response = build_success_response(

    question=question,

    rewritten_question=rewritten_question,

    answer=answer,

    followups=followups,

    verification=verification,

    confidence=confidence,

    dense_chunks=parent_chunks,

    expanded_chunks=expanded_chunks,

    compressed_chunks=compressed_chunks,

    results=results,

    bm25_chunks=bm25_chunks,

    hybrid_chunks=hybrid_chunks,

    sources=sources,

    citations=citations,

    context_chunks=context_chunks

)

    set_cache(

    question,

    response

)

    return response


from fastapi.responses import StreamingResponse
import json


def process_query_stream(question: str):

    logger = PerformanceLogger()

    logger.start("Pipeline")

    pipeline = run_retrieval_pipeline(question)

    logger.stop("Pipeline")

    rewritten_question = pipeline["rewritten_question"]
    query_type = pipeline["query_type"]
    config = pipeline["config"]
    metadata = pipeline["metadata"]
    queries = pipeline["queries"]

    logger.start("Dense Retrieval")

    results = retrieve_chunks(
        queries,
        metadata,
        config
    )

    logger.stop("Dense Retrieval")

    if not results:

        yield "data: ERROR\n\n"
        return

    context_data = build_context(
        question,
        results,
        config
    )

    sources = build_sources(results)

    dense_chunks = []

    for source in sources:

        dense_chunks.append({

            "text": source["text"],
            "page": source["page"],
            "document": source["document"],
            "chunk_id": source["chunk_id"],
            "parent_id": source["parent_id"],
            "vector_score": source["vector_score"],
            "retrieval_type": "dense"

        })

    bm25_results = bm25_search(

        query=question,

        document_name=metadata["document_name"],

        top_k=config["bm25_top_k"]

    )

    bm25_chunks = []

    for chunk, score in bm25_results:

        chunk = dict(chunk)

        chunk["retrieval_type"] = "bm25"

        chunk["bm25_score"] = float(score)

        bm25_chunks.append(chunk)

    hybrid_chunks = rrf_fusion(

        dense_chunks,

        bm25_chunks

    )

    ranked_chunks = rerank_chunks(

        question,

        hybrid_chunks

    )

    top_context = "\n\n".join(

        chunk["text"]

        for chunk in ranked_chunks[:5]

    )

    add_message(

        "user",

        question

    )

    logger.start("Generation")

    full_answer = ""

    for token in stream_answer(

        question,

        top_context,

        query_type

    ):

        full_answer += token

        yield f"data: {json.dumps({'token': token})}\n\n"

    logger.stop("Generation")

    add_message(

        "assistant",

        full_answer

    )

    logger.print_summary()

    yield "data: [DONE]\n\n"