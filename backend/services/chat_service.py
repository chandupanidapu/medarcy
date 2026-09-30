from backend.llm.router import router as llm_router


class ChatService:
    """
    Central AI orchestration service.

    Responsibilities:
    - Select LLM provider
    - Send prompts
    - Return generated responses

    Future extensions:
    - Streaming
    - Retry policies
    - Logging
    - Prompt templates
    - Context management
    """

    def __init__(self):
        self.router = llm_router

    async def generate_response(self, prompt: str) -> str:
        provider = self.router.get_provider()

        response = await provider.generate(prompt)

        return response


chat_service = ChatService()
