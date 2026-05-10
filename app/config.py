from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Prompt-It-Games"
    DATABASE_URL: str
    JWT_SECRET: str
    OPENAI_API_KEY: str
    REDIS_URL: str
    PYTHON_VERSION: str = "3.11"
    CORS_ORIGINS: str = "*"
    
    # 👇 AFEGEIX AQUESTA LÍNIA (Això és el que faltava) 👇
    RESEND_API_KEY: str = "" 

    class Config:
        env_file = ".env"

settings = Settings()
