from fastapi import APIRouter, HTTPException

from backend.models.request import ChatRequest
from backend.models.response import ChatResponse
from backend.services.chat_service import chat_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for Medarcy.

    Responsibilities:
    - Receive chat requests
    - Delegate AI generation to ChatService
    - Return standardized API responses
    """

    try:
        response = await chat_service.generate_response(request.prompt)

        return ChatResponse(
            provider="default",
            model="default",
            response=response,
            success=True,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
