import ollama

from app.services.chat_memory import (
    get_history
)


def generate_answer(
    question: str,
    context: str
):

    # Load Conversation History
    history = get_history()

    history_text = ""

    for msg in history:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
You are an Advanced RAG Assistant.

Rules:
1. Answer ONLY from the provided context.
2. Do not use outside knowledge.
3. Use conversation history only for understanding follow-up questions.
4. Do not make assumptions.
5. If answer is not present, say:
   "Insufficient information found."

CONVERSATION HISTORY:
{history_text}

CONTEXT:
{context}

QUESTION:
{question}
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

    return response["message"]["content"]