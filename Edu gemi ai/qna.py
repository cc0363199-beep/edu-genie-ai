from ai_service import ai


async def answer_question(question: str):

    prompt = f"""
Answer the following learner question.

Question:
{question}

Requirements:

1. Give the direct answer first.
2. Explain the answer clearly.
3. Use a simple example if useful.
4. Use numbered steps when appropriate.
5. Keep the answer educational and easy to understand.
"""

    return await ai.generate(prompt)