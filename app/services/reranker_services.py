from app.services.cross_encoder_service import (
    cross_encoder
)


def rerank_chunks(
    question,
    chunks
):

    if not chunks:
        return []

    # ==========================================
    # Prepare Cross Encoder Input
    # ==========================================

    pairs = [

        (question, chunk["text"])

        for chunk in chunks

    ]

    scores = cross_encoder.predict(
        pairs
    )

    ranked = []

    # ==========================================
    # Attach Score
    # ==========================================

    for chunk, score in zip(chunks, scores):

        chunk = dict(chunk)

        chunk["rerank_score"] = float(score)

        ranked.append(chunk)

    # ==========================================
    # Sort
    # ==========================================

    ranked.sort(

        key=lambda x: x["rerank_score"],

        reverse=True

    )

    return ranked