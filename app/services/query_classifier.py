def classify_query(question):

    q = question.lower()

    if "difference" in q or "compare" in q:
        return "COMPARISON"

    if "advantage" in q:
        return "ADVANTAGES"

    if "disadvantage" in q:
        return "DISADVANTAGES"

    if "steps" in q or "how to" in q:
        return "STEPS"

    if "explain" in q:
        return "EXPLANATION"

    if "list" in q:
        return "LIST"

    return "DEFINITION"