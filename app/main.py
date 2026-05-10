from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api import games
from app.database import engine, Base

# 👇 CLAU: Import explícit de la classe GameJob 👇
from app.models import GameJob

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 STARTUP: Checking database tables...")
    
    # Debug: quines taules ha detectat SQLAlchemy?
    detected = list(Base.metadata.tables.keys())
    print(f"📦 Tables detected: {detected}")
    
    if "game_jobs" not in detected:
        print("⚠️ WARNING: 'game_jobs' not found! Forcing registration...")
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created/verified!")
    except Exception as e:
        print(f"❌ Database error: {e}")
        raise
    
    yield

app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games.router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
