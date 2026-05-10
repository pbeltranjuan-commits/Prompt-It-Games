from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api import games
from app.database import engine, Base

# 👇 1. FORCEM LA IMPORTACIÓ DELS MODELS 👇
import app.models 

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 STARTUP: Initializing database...")
    
    # 👇 2. AIXÒ ÉS CRÍTIC: Ens dirà quines taules ha trobat 👇
    tables_found = list(Base.metadata.tables.keys())
    print(f"📦 TAULES DETECTADES: {tables_found}")
    
    if "game_jobs" not in tables_found:
        print("⚠️ ERROR CRÍTIC: No s'ha trobat la taula 'game_jobs'! Revisa els imports.")
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Taules creades/verificades correctament!")
    except Exception as e:
        print(f"❌ Error creant taules: {e}")
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
