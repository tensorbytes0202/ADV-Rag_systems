import ollama

from app.services.chat_memory import (
    get_history
)

def generate_answer(
    question: str,
    context: str
):

    history = get_history()

    history_text = ""

    for msg in history[-6:]:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
You are an Advanced RAG Assistant.

Rules:
1. Answer ONLY from provided context.
2. Do not use outside knowledge.
3. If answer is not found in context, reply:
   Insufficient information found.
4. Give concise answers.

CONVERSATION:
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

    answer = response["message"]["content"]

    print("\n" + "=" * 50)
    print("GENERATED ANSWER")
    print("=" * 50)
    print(answer)
    print("=" * 50 + "\n")

    return answer