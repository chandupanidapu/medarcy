import google.generativeai as genai

from core.config import settings
from llm.base import BaseLLM


class GeminiProvider(BaseLLM):

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate(self, prompt: str):

        response = self.model.generate_content(prompt)

        return response.text