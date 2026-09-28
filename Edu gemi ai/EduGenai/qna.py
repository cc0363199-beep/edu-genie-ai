from ai_service import ai


async def answer_question(question: str) -> str:
    prompt = f"""
Answer the following question clearly and simply for a student.

Question:
{question}

Give a helpful educational answer.
"""

    return await ai.generate(prompt)