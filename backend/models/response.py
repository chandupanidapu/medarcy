from typing import Optional

from pydantic import BaseModel


class ChatResponse(BaseModel):
    provider: str
    model: str
    response: str
    success: bool = True
    error: Optional[str] = None