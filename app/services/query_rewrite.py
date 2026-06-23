import ollama

from app.services.chat_memory import (
    get_history
)


def rewrite_question(
    question: str
):

    history = get_history()

    history_text = ""

    for msg in history[-6:]:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
Convert the follow-up question into a standalone question.

Conversation:
{history_text}

Question:
{question}

Only return the rewritten question.
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

    return response["message"]["content"].strip()