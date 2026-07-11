from app.services.llm_provider import chat

from app.prompts.generation_prompt import (
    build_generation_prompt
)


# ============================================================
# Normal Generation
# ============================================================

def generate_answer(
    question: str,
    context: str,
    query_type: str
):

    prompt = build_generation_prompt(
        question,
        context,
        query_type
    )

    response = chat(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    answer = response["message"]["content"]

    print("\n" + "=" * 60)
    print("GENERATED ANSWER")
    print("=" * 60)
    print(answer)
    print("=" * 60 + "\n")

    return answer


# ============================================================
# Streaming Generation
# ============================================================

def stream_answer(
    question: str,
    context: str,
    query_type: str
):

    prompt = build_generation_prompt(
        question,
        context,
        query_type
    )

    stream = chat(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        stream=True

    )

    for chunk in stream:

        if "message" in chunk:

            token = chunk["message"]["content"]

            yield token