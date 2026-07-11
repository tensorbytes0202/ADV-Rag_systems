from rank_bm25 import BM25Okapi

from app.services.bm25_index import (
    save_index,
    load_index
)


def build_bm25_index(
    document_name,
    chunks
):

    tokenized = [

        chunk["text"].split()

        for chunk in chunks

    ]

    bm25 = BM25Okapi(tokenized)

    save_index(
        document_name,
        bm25,
        chunks
    )


def bm25_search(

    query,

    document_name,

    top_k=10

):

    data = load_index(document_name)

    if data is None:
        return []

    bm25 = data["bm25"]
    chunks = data["chunks"]

    scores = bm25.get_scores(
        query.split()
    )

    ranked = sorted(

        zip(chunks, scores),

        key=lambda x: x[1],

        reverse=True

    )

    return ranked[:top_k]