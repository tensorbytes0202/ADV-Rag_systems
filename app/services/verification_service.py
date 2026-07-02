import json
import ollama


def verify_answer(
    question,
    answer,
    context
):

    prompt = f"""
You are an expert RAG verification system.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Task:

Verify whether the generated answer is fully supported by the retrieved context.

Return ONLY valid JSON in this format:

{{
    "supported": true,
    "confidence": 0.94,
    "reason": "Answer is completely supported by retrieved context."
}}

Rules:

- supported must be true or false
- confidence must be between 0 and 1
- reason must be one short sentence
- Do not return anything except JSON.
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

    content = response["message"]["content"].strip()

    try:

        result = json.loads(content)

    except Exception:

        result = {

            "supported": False,

            "confidence": 0.0,

            "reason": "Verification parsing failed."

        }

    return result