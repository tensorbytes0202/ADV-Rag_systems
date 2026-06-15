from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_chunks(
    question,
    chunks
):

    if not chunks:
        return []

    pairs = [
        (question, chunk)
        for chunk in chunks
    ]

    scores = reranker.predict(
        pairs
    )

    ranked = list(
        zip(chunks, scores)
    )

    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranked