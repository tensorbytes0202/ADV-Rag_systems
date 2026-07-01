from sentence_transformers import CrossEncoder

# ============================================
# Load Compression Model
# ============================================

compressor = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ============================================
# Context Compression
# ============================================

def compress_context(

    question,

    chunks,

    top_k=8

):
    """
    Compress expanded context using
    Cross Encoder relevance scoring.
    """

    if not chunks:
        return []

    pairs = [

        (question, chunk)

        for chunk in chunks

    ]

    scores = compressor.predict(pairs)

    ranked = list(

        zip(chunks, scores)

    )

    ranked.sort(

        key=lambda x: x[1],

        reverse=True

    )

    compressed = [

        chunk

        for chunk, _ in ranked[:top_k]

    ]

    return compressed