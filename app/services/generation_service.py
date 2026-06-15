import ollama


def generate_answer(
    question: str,
    context: str
):

    prompt = f"""
You are an Advanced RAG Assistant.

Rules:
1. Answer ONLY from the provided context.
2. Do not use outside knowledge.
3. Do not make assumptions.
4. If answer is not present, say:
   "Insufficient information found."

CONTEXT:
{context}

QUESTION:
{question}
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

    return response["message"]["content"]