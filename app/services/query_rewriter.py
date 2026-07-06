import json
import ollama


SYSTEM_PROMPT = """
Generate 5 different semantic versions of the user's query.

Rules:

- Same meaning
- Different wording
- No explanation
- Return JSON only

Example

{
    "queries":[
        "What is process?",
        "Define process.",
        "Explain process.",
        "Operating system process.",
        "Program in execution."
    ]
}
"""


def rewrite_query(question):

    response = ollama.chat(

        model="llama3:latest",

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

            "temperature": 0.2

        }

    )

    try:

        data = json.loads(

            response["message"]["content"]

        )

        return data["queries"]

    except:

        return [question]