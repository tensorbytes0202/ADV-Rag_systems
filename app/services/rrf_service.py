def rrf_fusion(
    dense_chunks,
    bm25_chunks,
    k=60
):

    scores = {}
    objects = {}

    # Dense
    for rank, chunk in enumerate(dense_chunks):

        key = chunk["text"]

        scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)

        objects[key] = chunk

    # BM25
    for rank, chunk in enumerate(bm25_chunks):

        key = chunk["text"]

        scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)

        if key not in objects:
            objects[key] = chunk

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        objects[text]
        for text, _ in ranked
    ]