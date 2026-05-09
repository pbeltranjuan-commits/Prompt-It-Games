from celery import shared_task
from sqlalchemy import select
from app.database import async_session
from app.models import GameJob, JobStatus
from app.services.ai_service import generate_rules, generate_images
from app.services.pdf_service import assemble_pdf
import structlog

logger = structlog.get_logger()

@shared_task(bind=True, max_retries=3)
def process_game_job(self, job_id: str, payload: dict):
    async def run():
        async with async_session() as db:
            job = (await db.execute(select(GameJob).where(GameJob.id == job_id))).scalar_one()
            job.status = JobStatus.PROCESSING
            await db.commit()
            logger.info("job_processing", job_id=job_id)

            try:
                rules = await generate_rules(payload)
                images = await generate_images(rules, payload["art_style"])
                pdf_url = await assemble_pdf(rules, images, job_id)
                job.status = JobStatus.COMPLETED
                job.result_url = pdf_url
                job.preview_url = pdf_url.replace(".pdf", "_preview.png")
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                logger.error("job_failed", job_id=job_id, error=str(e))
            await db.commit()

    import asyncio
    asyncio.run(run())
