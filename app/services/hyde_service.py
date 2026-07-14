from app.services.llm_provider import chat


def generate_hyde(question: str):

    prompt = f"""
Generate a concise hypothetical passage that would perfectly answer the question.

Question:
{question}

Return only the passage.
"""

    response = chat(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return response["message"]["content"].strip()