from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api import games
from app.database import engine, Base
import structlog, sentry_sdk

settings = get_settings()
structlog.configure(processors=[structlog.processors.JSONRenderer()])
sentry_sdk.init(dsn="https://...", traces_sample_rate=1.0)

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS.split(","), allow_methods=["*"], allow_headers=["*"])
app.include_router(games.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    structlog.get_logger().info("startup_complete")

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
