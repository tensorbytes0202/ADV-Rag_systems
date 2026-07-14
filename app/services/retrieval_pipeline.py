
import os

from app.services.query_rewriter import rewrite_query
from app.services.metadata_parser import extract_metadata
from app.services.document_registry import get_active_document
from app.services.query_classifier import classify_query
from app.services.query_router import get_retrieval_config
from app.services.hyde_service import generate_hyde
from app.services.embedding_service import (
    generate_query_embedding
)

from app.services.vector_store import (
    search_similar_chunks
)

from app.services.parent_retriever import (
    get_parent_chunks
)

from app.services.context_expansion import (
    expand_context
)

from app.services.context_compression import (
    compress_context
)
from app.services.self_query_service import generate_self_query
from app.services.query_decomposition import (
    decompose_query
)

# ==========================================================
# Retrieval Pipeline
# ==========================================================

def run_retrieval_pipeline(question: str):

    # ==========================================
    # Rewrite Query
    # ==========================================

    rewritten_question = rewrite_query(question)
    # ==========================================
    # Query Decomposition
    # ==========================================

    subqueries = decompose_query(question)

    # Rewrite output ko list bana do
    queries = []

    queries.extend(subqueries)

    if isinstance(rewritten_question, str):

        queries.append(rewritten_question)

    else:

        queries.extend(rewritten_question)

    if not queries:
        queries = [question]

    queries.append(question)

    # duplicate remove
    queries = list(dict.fromkeys(queries))
    

    # ==========================================
    # Metadata
    # ==========================================

    metadata = extract_metadata(question)
    # ==========================================
    # Self Query Retrieval
    # ==========================================

    self_query = generate_self_query(question)

    # LLM metadata has higher priority

    if self_query["document_name"]:

        metadata["document_name"] = self_query["document_name"]

    elif metadata["document_name"] is None:

        metadata["document_name"] = get_active_document()


    if self_query["page"]:

        metadata["page"] = self_query["page"]


    if self_query["chapter"]:

        metadata["chapter"] = self_query["chapter"]


    if self_query["section"]:

        metadata["section"] = self_query["section"]

    if metadata["document_name"]:

        metadata["document_name"] = os.path.basename(
            metadata["document_name"]
        ).strip()

    # ==========================================
    # Query Type
    # ==========================================

    query_type = classify_query(question)

    config = get_retrieval_config(query_type)

    hyde_document = None

    if config.get("use_hyde", False):

        hyde_document = generate_hyde(question)
        for subquery in subqueries:

            hyde = generate_hyde(subquery)

            queries.append(hyde)

    if hyde_document:

        queries.append(hyde_document)

    queries = list(dict.fromkeys(queries))

    return {

    "question": question,

    "rewritten_question": rewritten_question,

    "subqueries": subqueries,

    "metadata": metadata,

    "query_type": query_type,

    "config": config,

    "queries": queries,

    "hyde_document": hyde_document,

    "self_query": self_query

}


 


# ==========================================================
# Dense Retrieval
# ==========================================================

def retrieve_chunks(

    queries,

    metadata,

    config

):

    all_results = []

    for query in queries:

        embedding = generate_query_embedding(query)

        results = search_similar_chunks(

            embedding,

            limit=config["dense_top_k"],

            document_name=metadata["document_name"],

            page=metadata["page"]

        )

        all_results.extend(results)

    # =====================================
    # Remove Duplicate Chunks
    # =====================================

    unique = {}

    for result in all_results:

        payload = result.payload

        chunk_id = payload.get("chunk_id")

        if chunk_id not in unique:

            unique[chunk_id] = result

        elif result.score > unique[chunk_id].score:

            unique[chunk_id] = result

    results = list(unique.values())

    results.sort(

        key=lambda x: x.score,

        reverse=True

    )

    return results


# ==========================================================
# Build Retrieval Context
# ==========================================================

def build_context(

    question,

    results,

    config

):
# ===================================
# Parent Retrieval
# ===================================

    parent_chunks = get_parent_chunks(
        results
    )

    # ===================================
    # Context Expansion
    # ===================================

    expanded_chunks = expand_context(
        results,
        window_size=config["window_size"]
    )

    # ===================================
    # Context Compression
    # ===================================

    compressed_chunks = compress_context(

        question,

        expanded_chunks,

        top_k=config["compression_top_k"]

    )

    # ===================================
    # Final Context
    # ===================================

    context = "\n\n".join(
        compressed_chunks
    )

    return {

        "parent_chunks": parent_chunks,

        "expanded_chunks": expanded_chunks,

        "compressed_chunks": compressed_chunks,

        "context": context

    }
# ==========================================================
# Build Context Chunks
# ==========================================================

# ==========================================================
# Build Context Chunks
# ==========================================================

def build_context_chunks(

    ranked_chunks,

    top_k=5

):

    context_chunks = []

    for chunk in ranked_chunks[:top_k]:

        context_chunks.append({

    "text": chunk.get("text"),
    "page": chunk.get("page"),
    "document": chunk.get("document"),

    "chunk_id": chunk.get("chunk_id"),
    "parent_id": chunk.get("parent_id"),

    "vector_score": chunk.get("vector_score"),
    "bm25_score": chunk.get("bm25_score"),

    "retrieval_type": chunk.get("retrieval_type"),
    "rerank_score": chunk.get("rerank_score")

})

    return context_chunks

# ==========================================================
# Build Sources
# ==========================================================
def build_sources(results):

    sources = []

    seen = set()

    for result in results:

        payload = result.payload

        key = (

            payload.get("document_name"),

            payload.get("page"),

            payload.get("parent_id")

        )

        if key in seen:
            continue

        seen.add(key)

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

    "text": payload.get(
        "text",
        ""
    ),

    "parent_text": payload.get(
        "parent_text",
        ""
    ),

    "vector_score": float(
        result.score
    ),

    "retrieval_type": "dense"

})

    return sources


# ==========================================================
# Build Citations
# ==========================================================

def build_citations(

    sources,

    top_k=5

):

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

        if len(citations) == top_k:

            break

    return citations


# ==========================================================
# Convert BM25 Result -> Dense Format
# ==========================================================

# ==========================================================
# Convert BM25 Result
# ==========================================================

def convert_bm25_chunks(bm25_results):

    chunks = []

    for chunk, score in bm25_results:

        chunk = dict(chunk)

        chunk["retrieval_type"] = "bm25"

        chunk["bm25_score"] = float(score)

        chunks.append(chunk)

    return chunks