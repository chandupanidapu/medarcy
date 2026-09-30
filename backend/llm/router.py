from backend.core.config import settings

from backend.llm.claude import ClaudeProvider
from backend.llm.gemini import GeminiProvider
from backend.llm.openai import OpenAIProvider


class LLMRouter:

    def __init__(self):

        self.providers = {
            "gemini": GeminiProvider(),
            "openai": OpenAIProvider(),
            "claude": ClaudeProvider(),
        }

    def get_provider(self):

        return self.providers.get(
            settings.DEFAULT_PROVIDER,
            self.providers["gemini"],
        )


router = LLMRouter()
