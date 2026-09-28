from ai_service import ai


async def recommend_learning_path(
    topic: str,
    level: str = "beginner"
):

    prompt = f"""
Create a personalized learning path.

Topic:
{topic}

Learner level:
{level}

Include:

1. Prerequisites
2. Beginner concepts
3. Intermediate concepts
4. Advanced concepts
5. Practical exercises
6. A mini project
7. Suggested practice routine
8. What the learner should know before moving
   to the next level

Keep the plan realistic and educational.

Do not invent external links.
"""

    return await ai.generate(prompt)