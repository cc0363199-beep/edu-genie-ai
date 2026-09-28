import os

try:
    from google import genai
except ImportError:
    genai = None


SYSTEM_INSTRUCTION = """
You are EduGenie, an educational AI assistant.

Your job is to help students learn clearly and accurately.

Rules:

1. Explain concepts in simple language.
2. Use examples whenever useful.
3. Break difficult topics into steps.
4. Avoid unnecessary technical jargon.
5. Do not invent facts.
6. Do not invent sources or links.
7. If the question is ambiguous, state your assumption.
8. Adapt explanations to the learner's level.
"""


class AIService:

    def __init__(self):

        self.api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        self.client = None

        if self.api_key and genai is not None:

            self.client = genai.Client(
                api_key=self.api_key
            )

    @property
    def configured(self):

        return self.client is not None

    async def generate(self, prompt: str):

        # --------------------------------------------------
        # Gemini mode
        # --------------------------------------------------

        if self.client:

            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=(
                    SYSTEM_INSTRUCTION
                    + "\n\n"
                    + prompt
                ),
            )

            text = getattr(
                response,
                "text",
                None
            )

            if not text:

                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        # --------------------------------------------------
        # Offline mode
        # --------------------------------------------------

        return self.offline_fallback(prompt)

    @staticmethod
    def offline_fallback(prompt: str):

        prompt_lower = prompt.lower()

        if "summar" in prompt_lower:

            return (
                "Offline mode: Gemini is not configured.\n\n"
                "Add GEMINI_API_KEY to your .env file "
                "to enable AI summarization."
            )

        if "quiz" in prompt_lower:

            return (
                "Offline mode: Gemini is not configured.\n\n"
                "Add GEMINI_API_KEY to your .env file "
                "to enable AI quiz generation."
            )

        if (
            "learning path" in prompt_lower
            or "prerequisite" in prompt_lower
        ):

            return (
                "Offline mode: Gemini is not configured.\n\n"
                "Add GEMINI_API_KEY to your .env file "
                "to enable personalized learning recommendations."
            )

        return (
            "Offline mode: Gemini is not configured.\n\n"
            "Add GEMINI_API_KEY to your .env file "
            "and restart the server."
        )


ai = AIService()