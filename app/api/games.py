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
# NOU ENDPOINT: GENERACIÓ COMPLETA + EMAIL (Amb 3 Categories)
# NOTA: Autenticació desactivada temporalment per a proves
# ==============================================================================

@router.post("/generate-full", status_code=202)
async def generate_full_game(
    theme: str,
    difficulty: str = "medium",
    game_category: str = "board",  # NOU: "board", "card_game" o "rpg"
    user_email: str = "pbeltranjuan@gmail.com",
    db: AsyncSession = Depends(get_db),
    # user_id: str = Depends(get_current_user)  # ← COMENTAT PER PROVES
):
    """
    Flux complet amb 3 categories de joc:
    - board: Jocs de taula (taulers + fitxes)
    - card_game: Jocs de cartes (baralles completes)
    - rpg: Jocs de rol (fulls de personatge tipus revista)
    
    1. Genera assets segons la categoria
    2. Crea un ZIP amb tots els assets
    3. L'envia per correu a l'usuari
    4. Neteja els fitxers temporals
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    try:
        logger.info("start_generation", theme=theme, difficulty=difficulty, category=game_category)

        # === GENERACIÓ SEGONS CATEGORIA ===
        
        if game_category == "board":
            # 🎲 JOCS DE TAULA (el que ja tenies)
            logger.info("🎲 Generant Joc de Taula...")
            generate_card("poker", f"{theme} - Atac", f"Acció ofensiva de nivell {difficulty}")
            generate_card("poker", f"{theme} - Defensa", f"Acció defensiva de nivell {difficulty}")
            generate_board("square_8", f"Tauler: {theme}")

        elif game_category == "card_game":
            # 🃏 JOCS DE CARTES (NOU - Baralla completa)
            logger.info("🃏 Generant Joc de Cartes...")
            # Generem una baralla de 20 cartes (pots ajustar aquest número)
            for i in range(1, 21):
                generate_card("poker", f"{theme} - Carta {i}", f"Efecte especial {difficulty}")

        elif game_category == "rpg":
            # 📜 JOCS DE ROL (NOU - Fulls de personatge)
            logger.info("📜 Generant Joc de Rol (Character Sheets)...")
            # Generem 4 fulls de personatge tipus A4 (pots ajustar)
            for i in range(1, 5):
                generate_board("a4_sheet", f"{theme} - Personatge {i}\nClasse: {difficulty}")

        else:
            raise ValueError(f"Categoria '{game_category}' no reconeguda. Usa: board, card_game, rpg")

        # === COMPRIMIR EN ZIP ===
        zip_name = f"{theme.replace(' ', '_')}_{game_category}.zip"
        zip_path = create_zip(output_dir, zip_name)
        logger.info("zip_created", path=zip_path)

        # === ENVIAR PER CORREU (Simulat) ===
        await send_game_zip(user_email, zip_path, f"{theme} ({game_category})")
        logger.info("email_sent", to=user_email)

        return {
            "message": f"✅ {game_category} generat i enviat!", 
            "zip_name": zip_name,
            "sent_to": user_email,
            "category": game_category
        }
    
    except Exception as e:
        logger.error("generation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error intern: {str(e)}")
    
    finally:
        # === NETEJA: Esborra la carpeta temporal ===
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            logger.info("temp_files_cleaned")
