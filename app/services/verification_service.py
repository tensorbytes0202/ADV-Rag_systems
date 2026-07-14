import json

from app.services.llm_provider import chat


# ==========================================================
# Verify Generated Answer
# ==========================================================

def verify_answer(
    question: str,
    answer: str,
    context: str
):

    prompt = f"""
You are an expert RAG verification system.

Your job is to verify whether the generated answer is supported by the retrieved context.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Instructions:

- Compare ONLY with the retrieved context.
- Do NOT use outside knowledge.
- If the answer is fully supported, return supported=true.
- If partially supported, supported=false.
- Return ONLY valid JSON.

Example:

{{
    "supported": true,
    "confidence": 0.94,
    "reason": "The answer is fully supported by the retrieved context."
}}
"""

    response = chat(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0

    )

    content = response["message"]["content"].strip()

    try:

        return json.loads(content)

    except Exception:

        return {

            "supported": False,

            "confidence": 0.0,

            "reason": "Verification parsing failed."

        }