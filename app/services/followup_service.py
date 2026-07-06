import ollama


def generate_followups(question, answer):

    try:

        prompt = f"""
You are an expert teacher.

User Question:
{question}

Answer:
{answer}

Generate exactly 5 follow-up questions.

Rules:
- Only questions
- One question per line
- No numbering
- No explanation
"""

        response = ollama.chat(

            model="llama3:latest",

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

    except Exception as e:

        print("FOLLOWUP ERROR:", e)

        return []