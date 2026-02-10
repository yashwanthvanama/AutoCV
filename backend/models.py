"""
Database models for AutoCV
"""
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from datetime import datetime
import uuid
from database import Base


class URLSubmissionModel(Base):
    """
    SQLAlchemy model for storing job description submissions
    This maps to the 'url_submissions' table in PostgreSQL
    """
    __tablename__ = "url_submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_description = Column(String, nullable=False, index=True)
    role = Column(String(50), nullable=True)
    embedding = Column(Vector(768), nullable=True)  # 768-dimensional vector embeddings
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<JobDescriptionSubmission(id={self.id}, role={self.role})>"
