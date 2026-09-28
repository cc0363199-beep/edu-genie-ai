from ai_service import ai


async def generate_quiz(topic: str, num_questions: int = 5) -> str:
    prompt = f"""
Create a simple educational quiz for a student.

Topic: {topic}
Number of questions: {num_questions}

For each question, provide:
1. The question
2. Four options (A, B, C, D)
3. The correct answer

Keep the questions clear and suitable for a student.
"""

    return await ai.generate(prompt)