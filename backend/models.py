"""
Database models for AutoCV
"""
from sqlalchemy import Column, String, DateTime, Boolean, text
from pgvector.sqlalchemy import Vector
from datetime import datetime
from database import Base


class URLSubmissionModel(Base):
    """
    SQLAlchemy model for storing job description submissions
    This maps to the 'url_submissions' table in PostgreSQL
    """
    __tablename__ = "url_submissions"
    
    id = Column(String(20), primary_key=True, server_default=text("'JD-' || nextval('jd_id_seq')"))
    job_description = Column(String, nullable=False, index=True)
    role = Column(String(50), nullable=True)
    embedding = Column(Vector(768), nullable=True)  # 768-dimensional vector embeddings
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<JobDescriptionSubmission(id={self.id}, role={self.role})>"
