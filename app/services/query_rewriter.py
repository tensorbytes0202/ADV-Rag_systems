import json

from app.services.llm_provider import chat


SYSTEM_PROMPT = """
Generate ONLY 2 semantic rewrites of the user's query.

Rules:

- Preserve meaning
- Different wording
- No explanation
- Return ONLY JSON

Example:

{
    "queries": [
        "...",
        "..."
    ]
}
"""


def rewrite_query(question):

    response = chat(

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": question
            }

        ],

        temperature=0.2

    )

    try:

        data = json.loads(
            response["message"]["content"]
        )

        return data["queries"][:2]

    except Exception:

        return [question]