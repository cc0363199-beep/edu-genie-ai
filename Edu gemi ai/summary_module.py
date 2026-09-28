from ai_service import ai


async def summarize_text(text: str):

    prompt = f"""
Summarize the following learning material.

Material:
{text}

Return the following:

1. A short overview
2. Five key points
3. Important terms to remember

Do not add information that is not supported
by the supplied material.
"""

    return await ai.generate(prompt)