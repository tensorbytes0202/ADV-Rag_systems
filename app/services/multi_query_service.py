from app.services.llm_provider import chat


def generate_queries(question):

    prompt = f"""
Generate 4 alternative search queries.

Rules:

- Same meaning.
- Same domain.
- Do NOT number the queries.
- Do NOT use bullets.
- Do NOT write explanations.
- Return ONLY one query per line.

Question:
{question}
"""

    response = chat(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]

    queries = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # remove bullets

        if line.startswith("-"):
            line = line[1:].strip()

        if line.startswith("*"):
            line = line[1:].strip()

        # remove numbering

        if "." in line:

            left = line.split(".", 1)[0]

            if left.isdigit():

                line = line.split(".", 1)[1].strip()

        # ignore headings

        lower = line.lower()

        if "alternative search queries" in lower:
            continue

        if "here are" in lower:
            continue

        queries.append(line)

    # remove duplicates

    final_queries = []

    seen = set()

    final_queries.append(question)

    seen.add(question.lower())

    for q in queries:

        if q.lower() not in seen:

            seen.add(q.lower())

            final_queries.append(q)

    return final_queries[:5]