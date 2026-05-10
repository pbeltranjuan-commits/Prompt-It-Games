import os
import shutil
import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Imports dels teus mòduls locals
from app.database import get_db
from app.models import GameJob, JobStatus
from app.schemas import GameCreate, JobOut, JobStatusOut
from app.dependencies import get_current_user

# Imports del nou sistema de generació
from app.generator import generate_card, generate_board
from app.zipper import create_zip
from app.email_service import send_game_zip

logger = structlog.get_logger()
router = APIRouter(prefix="/api/games", tags=["games"])

# ==============================================================================
# ENDPOINTS EXISTENTS (Mantenim la funcionalitat de la base de dades)
# ==============================================================================

@router.post("/", response_model=JobOut, status_code=202)
async def create_job(
    data: GameCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """Crea una nova tasca de generació de joc (MVP Bàsic)"""
    job = GameJob(user_id=user_id, payload=data.model_dump_json())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    logger.info("job_created", job_id=str(job.id), user=user_id)
    
    return JobOut(
        job_id=job.id, 
        status=job.status, 
        message="Tasca creada. Generant joc..."
    )

@router.get("/{job_id}", response_model=JobStatusOut)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    """Obté l'estat actual d'una tasca"""
    job = (await db.execute(select(GameJob).where(GameJob.id == job_id))).scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    
    # Mapeig simple de progrés
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

# ==============================================================================
# NOU ENDPOINT: GENERACIÓ COMPLETA + EMAIL (La Màgia Real)
# NOTA: Autenticació desactivada temporalment per a proves
# ==============================================================================

@router.post("/generate-full", status_code=202)
async def generate_full_game(
    theme: str,
    difficulty: str = "medium",
    user_email: str = "pbeltranjuan@gmail.com",
    db: AsyncSession = Depends(get_db),
    # user_id: str = Depends(get_current_user)  # ← COMENTAT PER PROVES
):
    """
    Flux complet (versió de proves sense auth):
    1. Genera cartes i taulers (PNGs 300 DPI)
    2. Crea un ZIP amb tots els assets
    3. L'envia per correu a l'usuari
    4. Neteja els fitxers temporals
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    try:
        logger.info("start_generation", theme=theme, difficulty=difficulty)

        # 1. GENERAR ASSETS (Simulació d'IA per ara)
        # Generem 2 cartes tipus Poker
        generate_card("poker", f"{theme} - Atac", f"Acció ofensiva de nivell {difficulty}")
        generate_card("poker", f"{theme} - Defensa", f"Acció defensiva de nivell {difficulty}")
        
        # Generem 1 tauler 8x8
        generate_board("square_8", f"Tauler: {theme}")

        # 2. COMPRIMIR EN ZIP
        zip_name = f"{theme.replace(' ', '_')}_assets.zip"
        zip_path = create_zip(output_dir, zip_name)
        logger.info("zip_created", path=zip_path)

        # 3. ENVIAR PER CORREU
        await send_game_zip(user_email, zip_path, theme)
        logger.info("email_sent", to=user_email)

        return {
            "message": "✅ Joc generat i enviat al correu!", 
            "zip_name": zip_name,
            "sent_to": user_email
        }
    
    except Exception as e:
        logger.error("generation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error intern: {str(e)}")
    
    finally:
        # 4. NETEJA: Esborra la carpeta temporal per no saturar Render
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            logger.info("temp_files_cleaned")
