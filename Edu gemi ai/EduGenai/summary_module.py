from ai_service import ai


async def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following text clearly and simply for a student.

Text:
{text}

Give a short, useful educational summary.
"""

    return await ai.generate(prompt)