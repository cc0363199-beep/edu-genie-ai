from ai_service import ai


async def explain_topic(topic: str):

    prompt = f"""
Explain the following topic as an educational lesson.

Topic:
{topic}

Use this structure:

1. Simple definition
2. How it works
3. Easy example
4. Important points
5. Short recap

Use simple language suitable for a student.
"""

    return await ai.generate(prompt)