def calculate_confidence(
    rerank_scores
):

    if not rerank_scores:
        return 0.0

    best_score = max(
        rerank_scores
    )

    confidence = min(
        best_score / 10,
        1.0
    )

    return round(
        confidence,
        2
    )