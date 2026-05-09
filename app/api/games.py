from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import GameJob, JobStatus
from app.schemas import GameCreate, JobOut, JobStatusOut
from app.dependencies import get_current_user
import structlog

logger = structlog.get_logger()
router = APIRouter(prefix="/api/games", tags=["games"])

@router.post("/", response_model=JobOut, status_code=202)
async def create_job(
    data: GameCreate,  # ← CORREGIT: ara sí que té "data:"
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """Crea una nova tasca de generació de joc"""
    job = GameJob(user_id=user_id, payload=data.model_dump_json())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    # Celery: comentat temporalment fins que estigui configurat
    # from app.tasks.tasks import process_game_job
    # process_game_job.delay(str(job.id), data.model_dump())
    
    logger.info("job_created", job_id=str(job.id), user=user_id)
    return JobOut(job_id=job.id, status=job.status, message="Generant joc...")

@router.get("/{job_id}", response_model=JobStatusOut)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    """Obté l'estat actual d'una tasca"""
    job = (await db.execute(select(GameJob).where(GameJob.id == job_id))).scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    
    # Calcula el progress correctament
    progress_map = {
        JobStatus.QUEUED: 10,
        JobStatus.PROCESSING: 50,
        JobStatus.COMPLETED: 100,
        JobStatus.FAILED: 0
    }
    progress = progress_map.get(job.status, 0)
    
    return JobStatusOut(
        job_id=job.id,
        status=job.status,
        progress=progress,
        result_url=job.result_url,
        preview_url=job.preview_url,
        error=job.error,
        created_at=job.created_at,
        updated_at=job.updated_at
    )
