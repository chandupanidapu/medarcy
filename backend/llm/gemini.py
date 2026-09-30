from google import genai

from backend.core.config import settings
from backend.llm.base import BaseLLM


class GeminiProvider(BaseLLM):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"

    async def generate(self, prompt: str) -> str:
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text or ""
