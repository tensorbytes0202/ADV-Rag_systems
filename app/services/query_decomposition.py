import json

from app.services.llm_provider import chat


SYSTEM_PROMPT = """
You are an expert query planner.

If the question contains multiple sub-questions,
split it into independent retrieval queries.

Rules:

- Return JSON only
- Maximum 5 subqueries
- If decomposition is unnecessary,
return the original question only.

Example:

{
    "subqueries":[
        "What is Process Scheduling?",
        "What is Thread Scheduling?",
        "Compare Process Scheduling and Thread Scheduling."
    ]
}
"""


def decompose_query(question: str):

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

        temperature=0

    )

    try:

        data = json.loads(
            response["message"]["content"]
        )

        return data["subqueries"]

    except Exception:

        return [question]