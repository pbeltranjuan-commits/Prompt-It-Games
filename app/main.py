from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api import games
from app.database import engine, Base

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclou el router
app.include_router(games.router)

# Startup: crea taules a la BD
@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Startup complete - Database tables created")
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        raise

# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
