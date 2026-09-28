from ai_service import ai


async def recommend_learning_path(topic: str) -> str:
    prompt = f"""
Create a simple learning path for a student.

Topic:
{topic}

Include:
1. Beginner concepts
2. Intermediate concepts
3. Advanced concepts
4. Practice suggestions

Keep it clear and easy for a student to follow.
"""

    return await ai.generate(prompt)