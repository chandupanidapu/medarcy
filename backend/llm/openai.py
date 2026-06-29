from llm.base import BaseLLM


class OpenAIProvider(BaseLLM):

    async def generate(self, prompt: str):
        raise NotImplementedError("OpenAI provider coming soon.")