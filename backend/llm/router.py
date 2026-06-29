from core.config import settings

from llm.gemini import GeminiProvider
from llm.openai import OpenAIProvider
from llm.claude import ClaudeProvider


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