from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Prompt-It-Games"
    DATABASE_URL: str
    JWT_SECRET: str
    OPENAI_API_KEY: str
    REDIS_URL: str
    PYTHON_VERSION: str = "3.11"
    CORS_ORIGINS: str = "*"
    RESEND_API_KEY: str = ""

    class Config:
        env_file = ".env"

# Instància global
settings = Settings()

# Funció que el teu codi necessita importar
def get_settings() -> Settings:
    return settings
