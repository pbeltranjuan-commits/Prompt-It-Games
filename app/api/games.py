from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import GameJob, JobStatus
from app.schemas import GameCreate, JobOut, JobStatusOut
from app.dependencies import get_current_user
from app.tasks.tasks import process_game_job
import structlog

logger = structlog.get_logger()
router = APIRouter(prefix="/api/games", tags=["games"])

@router.post("/", response_model=JobOut, status_code=202)
async def create_job(
    data: GameCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    job = GameJob(user_id=user_id, payload=data.model_dump_json())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    process_game_job.delay(str(job.id), data.model_dump())
    logger.info("job_created", job_id=str(job.id), user=user_id)
    return JobOut(job_id=job.id, status=job.status, message="Generant joc...")

@router.get("/{job_id}", response_model=JobStatusOut)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    job = (await db.execute(select(GameJob).where(GameJob.id == job_id))).scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Tasca no trobada")
    return JobStatusOut(
        job_id=job.id, status=job.status, progress=job.status.value == JobStatus.COMPLETED and 100 or 30,
        result_url=job.result_url, preview_url=job.preview_url, error=job.error
    )
