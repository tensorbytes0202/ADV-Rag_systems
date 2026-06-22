from rank_bm25 import BM25Okapi


def bm25_search(
    query,
    chunks,
    top_k=20,
    document_filter=None
):

    filtered_chunks = []

    for chunk in chunks:

        if document_filter:

            if (
                chunk["document"]
                != document_filter
            ):
                continue

        filtered_chunks.append(
            chunk
        )

    if not filtered_chunks:
        return []

    tokenized_chunks = [

        chunk["text"].split()

        for chunk in filtered_chunks
    ]

    bm25 = BM25Okapi(
        tokenized_chunks
    )

    tokenized_query = query.split()

    scores = bm25.get_scores(
        tokenized_query
    )

    ranked = sorted(
        zip(filtered_chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_k]