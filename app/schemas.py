from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models import JobStatus

class GameCreate(BaseModel):
    """Esquema per crear un nou joc"""
    theme: str = Field(..., min_length=1, max_length=200, description="Tema del joc")
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$", description="Dificultat")
    num_questions: int = Field(default=10, ge=5, le=50, description="Nombre de preguntes")
    language: str = Field(default="ca", description="Idioma")

class JobOut(BaseModel):
    """Resposta després de crear una tasca"""
    job_id: UUID
    status: JobStatus
    message: str
    
    model_config = {
        "from_attributes": True
    }

class JobStatusOut(BaseModel):
    """Estat actual d'una tasca"""
    job_id: UUID
    status: JobStatus
    progress: int
    result_url: Optional[str] = None
    preview_url: Optional[str] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }
