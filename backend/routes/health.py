from fastapi import APIRouter

from backend.models.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
    )
