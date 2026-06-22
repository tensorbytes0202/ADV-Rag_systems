import ollama


def verify_answer(
    question,
    answer,
    context
):

    prompt = f"""
QUESTION:
{question}

ANSWER:
{answer}

CONTEXT:
{context}

Is every important claim in the answer
supported by the context?

Return ONLY:

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

    return (
        response["message"]["content"]
        .strip()
        .upper()
    )