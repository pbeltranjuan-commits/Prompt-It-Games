from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "AI Board Game Generator"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/boardgames"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    REPLICATE_API_TOKEN: str = ""
    S3_BUCKET: str = "ai-games-prod"
    S3_ENDPOINT: str = "https://s3.amazonaws.com"
    JWT_SECRET: str = ""
    CORS_ORIGINS: str = "https://app.eldteudomini.com"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
