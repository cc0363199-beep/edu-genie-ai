import json
import re

from ai_service import ai


def extract_json(text: str):

    text = text.strip()

    # Remove Markdown code fences if Gemini adds them
    fenced = re.search(
        r"```(?:json)?\s*(\{.*\})\s*```",
        text,
        re.DOTALL
    )

    if fenced:

        candidate = fenced.group(1)

    else:

        candidate = text

    start = candidate.find("{")
    end = candidate.rfind("}")

    if start >= 0 and end > start:

        candidate = candidate[
            start:end + 1
        ]

    return json.loads(candidate)


async def generate_quiz(
    topic: str,
    count: int = 3
):

    prompt = f"""
Create a multiple-choice quiz about:

{topic}

Create exactly {count} questions.

Each question must have exactly four options.

Exactly one option must be correct.

Return ONLY valid JSON using this format:

{{
    "title": "string",
    "questions": [
        {{
            "question": "string",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": 0,
            "explanation": "string"
        }}
    ]
}}

The answer is the zero-based index
of the correct option.
"""

    raw = await ai.generate(prompt)

    # Offline mode
    if raw.startswith("Offline mode:"):

        return {
            "title": f"{topic} Quiz",
            "questions": [],
            "message": raw
        }

    try:

        data = extract_json(raw)

    except (
        ValueError,
        json.JSONDecodeError
    ):

        return {
            "title": f"{topic} Quiz",
            "questions": [],
            "message": (
                "The AI returned an invalid quiz format. "
                "Please try again."
            ),
            "raw": raw
        }

    questions = data.get(
        "questions",
        []
    )

    clean_questions = []

    for question in questions[:count]:

        options = question.get(
            "options",
            []
        )

        answer = question.get(
            "answer"
        )

        if (
            isinstance(
                question.get("question"),
                str
            )
            and isinstance(
                options,
                list
            )
            and len(options) == 4
            and isinstance(
                answer,
                int
            )
            and 0 <= answer < 4
        ):

            clean_questions.append(
                {
                    "question":
                        question["question"],

                    "options":
                        [
                            str(option)
                            for option in options
                        ],

                    "answer":
                        answer,

                    "explanation":
                        str(
                            question.get(
                                "explanation",
                                ""
                            )
                        )
                }
            )

    return {
        "title":
            str(
                data.get(
                    "title",
                    f"{topic} Quiz"
                )
            ),

        "questions":
            clean_questions
    }