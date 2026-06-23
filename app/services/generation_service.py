import ollama

from app.services.chat_memory import (
    get_history
)


def generate_answer(
    question: str,
    context: str,
    query_type: str
):

    history = get_history()

    history_text = ""

    for msg in history[-6:]:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    # ===================================
    # Dynamic Formatting Instructions
    # ===================================

    format_instruction = ""

    if query_type == "COMPARISON":

        format_instruction = """
Answer in a comparison table.

Columns:
Feature | Item 1 | Item 2
"""

    elif query_type == "ADVANTAGES":

        format_instruction = """
Answer using bullet points.
"""

    elif query_type == "DISADVANTAGES":

        format_instruction = """
Answer using bullet points.
"""

    elif query_type == "STEPS":

        format_instruction = """
Answer step-by-step using numbered points.
"""

    elif query_type == "LIST":

        format_instruction = """
Answer using bullet points.
"""

    elif query_type == "EXPLANATION":

        format_instruction = """
Give a detailed explanation using headings and bullet points.
"""

    else:

        format_instruction = """
Give a concise answer.
"""

    # ===================================
    # Prompt
    # ===================================

    prompt = f"""
You are an Advanced RAG Assistant.

Rules:
1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. If answer is not found in context, reply exactly:
   Insufficient information found.
4. Follow the formatting instructions strictly.
5. Do not hallucinate.
6. Do not invent facts.
7. Use only the retrieved context.

FORMAT INSTRUCTION:
{format_instruction}

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

    answer = response["message"]["content"]

    print("\n" + "=" * 50)
    print("GENERATED ANSWER")
    print("=" * 50)
    print(answer)
    print("=" * 50 + "\n")

    return answer