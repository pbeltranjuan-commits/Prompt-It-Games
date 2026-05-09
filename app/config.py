from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Config per a Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # App
    APP_NAME: str = "AI Board Game Generator"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Base de dades (OBLIGATÒRIA - sense valor per defecte)
    DATABASE_URL: str
    
    # Redis (OBLIGATÒRIA)
    REDIS_URL: str
    
    # APIs externes
    OPENAI_API_KEY: str = ""
    REPLICATE_API_TOKEN: str = ""
    
    # AWS S3
    S3_BUCKET: str = "ai-games-prod"
    S3_ENDPOINT: str = "https://s3.amazonaws.com"
    
    # Autenticació
    JWT_SECRET: str
    
    # CORS
    CORS_ORIGINS: str = "*"

@lru_cache()
def get_settings():
    return Settings()
