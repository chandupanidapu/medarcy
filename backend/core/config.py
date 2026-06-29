from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "MediAgent"
    APP_VERSION: str = "1.0.0"

    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    DEFAULT_PROVIDER: str = "gemini"

    TEMPERATURE: float = 0.2
    MAX_TOKENS: int = 4096

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()