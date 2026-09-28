import os
from dotenv import load_dotenv

load_dotenv()


class AIService:
    async def generate(self, prompt: str) -> str:
        # Temporary response so the FastAPI project can run.
        # We will connect the real AI API after the server works.
        return f"AI response for: {prompt}"


ai = AIService()