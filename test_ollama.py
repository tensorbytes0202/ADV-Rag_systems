from app.services.generation_service import generate_answer

context = """
Hadoop is an open-source framework used for distributed
storage and processing of large datasets.
"""

answer = generate_answer(
    "What is Hadoop?",
    context
)

print(answer)