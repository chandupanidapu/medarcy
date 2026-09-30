from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.chat import router as chat_router
from backend.routes.health import router as health_router

app = FastAPI(
    title="Medarcy API",
    version="1.0.0",
    description="Open-source AI Clinical & Medical Research Assistant",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "application": "Medarcy",
        "status": "running",
        "version": "1.0.0",
    }


app.include_router(health_router)
app.include_router(chat_router)
