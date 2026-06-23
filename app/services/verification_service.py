import ollama


def verify_answer(
    question,
    answer,
    context
):

    prompt = f"""
You are a fact-checking system.

Question:
{question}

Answer:
{answer}

Context:
{context}

Task:
Check whether every important claim in the answer is supported by the context.

Return ONLY one word:

SUPPORTED

or

UNSUPPORTED
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

    result = (
        response["message"]["content"]
        .strip()
        .upper()
    )

    if "SUPPORTED" in result and "UNSUPPORTED" not in result:
        return "SUPPORTED"

    return "UNSUPPORTED"