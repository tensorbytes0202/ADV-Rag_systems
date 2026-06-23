import ollama


def generate_queries(question):

    prompt = f"""
You are helping an Operating System RAG system.

Generate 4 alternative search queries.

Rules:
1. Keep same meaning.
2. Stay in Operating System / Computer Science domain.
3. Do not change domain.
4. Return only queries.
5. One query per line.


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