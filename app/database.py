from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

# Defineix i exporta el Base (IMPORTANT!)
class Base(DeclarativeBase):
    pass

# Crea l'engine async
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Configura la sessió
async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Funció per obtenir la sessió de DB
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
