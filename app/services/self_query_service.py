import json

from app.services.llm_provider import chat


def generate_self_query(question: str):

    prompt = f"""
You are an intelligent query parser.

Extract structured search filters from the user's question.

Return ONLY valid JSON.

Schema:

{{
    "query": "",
    "document_name": null,
    "page": null,
    "chapter": null,
    "section": null,
    "topic": null
}}

Question:

{question}
"""

    response = chat(

    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]

)

    content = response["message"]["content"].strip()

    try:
        return json.loads(content)

    except Exception:

        return {

            "query": question,

            "document_name": None,

            "page": None,

            "chapter": None,

            "section": None,

            "topic": None

        }