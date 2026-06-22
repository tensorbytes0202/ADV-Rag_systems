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
Rewrite the question ONLY if it depends on previous conversation.

If question is already complete,
return it unchanged.

Conversation:
{history_text}

Question:
{question}

Return only rewritten question.
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