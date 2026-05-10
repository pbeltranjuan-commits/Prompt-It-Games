from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from app.database import Base

class JobStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GameJob(Base):
    __tablename__ = "game_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.QUEUED)
    payload = Column(Text)
    result_url = Column(String)
    preview_url = Column(String)
    error = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
