import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import URLSubmissionModel


def find_most_similar_job(new_embedding: list, db: Session, exclude_id: str = None):
    if exclude_id:
        query = text("""
            SELECT id, job_description, role, embedding,
                   1 - (embedding <=> :embedding) as similarity
            FROM url_submissions
            WHERE embedding IS NOT NULL AND id != :exclude_id
            ORDER BY embedding <=> :embedding
            LIMIT 1
        """)
        result = db.execute(query, {"embedding": str(new_embedding), "exclude_id": exclude_id}).fetchone()
    else:
        query = text("""
            SELECT id, job_description, role, embedding,
                   1 - (embedding <=> :embedding) as similarity
            FROM url_submissions
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> :embedding
            LIMIT 1
        """)
        result = db.execute(query, {"embedding": str(new_embedding)}).fetchone()
    
    if not result:
        return None, None
    
    most_similar_job = db.query(URLSubmissionModel).filter(
        URLSubmissionModel.id == result.id
    ).first()
    
    return most_similar_job, float(result.similarity)
