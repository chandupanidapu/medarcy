from llm.base import BaseLLM


class ClaudeProvider(BaseLLM):

    async def generate(self, prompt: str):
        raise NotImplementedError("Claude provider coming soon.")