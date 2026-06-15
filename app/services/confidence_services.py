def calculate_confidence(
    rerank_scores
):

    if not rerank_scores:
        return 0.0

    avg_score = sum(
        rerank_scores
    ) / len(rerank_scores)

    confidence = min(
        avg_score / 10,
        1.0
    )

    return round(
        confidence,
        2
    )