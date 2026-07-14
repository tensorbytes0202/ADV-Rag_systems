import json
from app.services.llm_provider import chat


SYSTEM_PROMPT = """
You are a Query Classification Engine.

Classify the user's question into ONLY ONE category.

Categories:

DEFINITION
EXPLANATION
COMPARISON
LIST
PROCEDURE
SUMMARY
CODE
FACTUAL

Return ONLY valid JSON.

Example:

{
    "query_type": "DEFINITION"
}
"""


def classify_query(question: str):

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

        options={
            "temperature": 0
        }

    )

    try:

        result = json.loads(
            response["message"]["content"]
        )

        return result["query_type"]

    except Exception:

        return "EXPLANATION"