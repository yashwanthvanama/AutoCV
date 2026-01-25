"""
Database models for AutoCV
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base


class URLSubmissionModel(Base):
    """
    SQLAlchemy model for storing URL submissions
    This maps to the 'url_submissions' table in PostgreSQL
    """
    __tablename__ = "url_submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False, index=True)
    role = Column(String(50), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<URLSubmission(id={self.id}, url={self.url})>"
