def rrf_fusion(
    dense_chunks,
    bm25_chunks,
    k=60
):

    scores = {}

    # Dense Rank Score
    for rank, chunk in enumerate(
        dense_chunks
    ):

        scores[chunk] = (
            scores.get(chunk, 0)
            + 1 / (k + rank + 1)
        )

    # BM25 Rank Score
    for rank, chunk in enumerate(
        bm25_chunks
    ):

        scores[chunk] = (
            scores.get(chunk, 0)
            + 1 / (k + rank + 1)
        )

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        chunk
        for chunk, score in ranked
    ]