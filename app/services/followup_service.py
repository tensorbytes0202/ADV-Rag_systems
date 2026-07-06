import ollama


def generate_followups(question, answer):

    prompt = f"""
You are an expert teacher.

User Question:
{question}

Answer:
{answer}

Generate exactly 5 intelligent follow-up questions.

Rules:
- Only questions
- One per line
- No numbering
- No explanations
- Maximum 12 words each
"""

    response = ollama.chat(

        model="llama3.2",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    text = response["message"]["content"]

    questions = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = line.lstrip("1234567890.- ")

        questions.append(line)

    return questions[:5]