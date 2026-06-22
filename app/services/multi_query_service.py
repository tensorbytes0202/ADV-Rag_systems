import ollama


def generate_queries(question):

    prompt = f"""
Generate 4 different search queries for the question.

Question:
{question}

Return only queries.
One per line.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    queries = response["message"]["content"].split("\n")

    queries = [
        q.strip()
        for q in queries
        if q.strip()
    ]

    queries.insert(0, question)

    return queries