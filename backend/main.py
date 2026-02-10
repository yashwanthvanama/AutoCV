from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from typing import Optional
import uvicorn
import os
from pathlib import Path

# Import database components
from database import get_db, engine, Base
from models import URLSubmissionModel
from template_manager import compile_template_to_pdf
from embeddings import generate_job_description_embedding
from similarity_finder import find_most_similar_job

# Create database tables
# This will create all tables defined in models.py if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AutoCV API",
    description="Backend API for AutoCV - URL submission service",
    version="1.0.0"
)

# CORS Configuration
# This allows your React app (running on a different port) to make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for request validation
# This ensures the data coming from the frontend is in the correct format
class JobDescriptionSubmission(BaseModel):
    job_description: str  # Job description text content
    role: str  # Job role selection
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_description": "We are seeking a skilled Software Engineer with 5+ years of experience...",
                "role": "Software Engineer"
            }
        }

# Response model
class JobDescriptionResponse(BaseModel):
    success: bool
    message: str
    job_description: str
    
# Root endpoint - just to check if the API is running
@app.get("/")
def read_root():
    return {
        "message": "Welcome to AutoCV API",
        "status": "running",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Endpoint to get all submitted job descriptions
@app.get("/api/job-descriptions")
async def get_all_job_descriptions(db: Session = Depends(get_db)):
    """
    Retrieve all job descriptions from the database.
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        List of all submitted job descriptions
    """
    try:
        submissions = db.query(URLSubmissionModel).order_by(
            URLSubmissionModel.submitted_at.desc()
        ).all()
        
        return {
            "success": True,
            "count": len(submissions),
            "submissions": [
                {
                    "id": str(submission.id),
                    "job_description": submission.job_description,
                    "role": submission.role,
                    "submitted_at": submission.submitted_at.isoformat()
                }
                for submission in submissions
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving job descriptions: {str(e)}"
        )


# Endpoint to delete a job description by ID
@app.delete("/api/job-descriptions/{submission_id}")
async def delete_job_description(submission_id: str, db: Session = Depends(get_db)):
    """
    Delete a job description from the database by its ID and remove associated files.
    
    Args:
        submission_id: UUID of the job description to delete
        db: Database session (injected by FastAPI)
        
    Returns:
        Success message
    """
    try:
        # Find the submission by ID
        submission = db.query(URLSubmissionModel).filter(
            URLSubmissionModel.id == submission_id
        ).first()
        
        if not submission:
            raise HTTPException(
                status_code=404,
                detail=f"Job description with ID {submission_id} not found"
            )
        
        # Delete the record from database
        db.delete(submission)
        db.commit()
        
        # Delete the associated folder and its contents
        resumes_dir = Path(__file__).parent.parent / "resumes"
        record_folder = resumes_dir / submission_id
        
        if record_folder.exists() and record_folder.is_dir():
            try:
                import shutil
                shutil.rmtree(record_folder)
                print(f"Deleted folder: {record_folder}")
            except Exception as folder_error:
                print(f"Warning: Could not delete folder {record_folder}: {folder_error}")
                # Don't fail the request if folder deletion fails
        
        return {
            "success": True,
            "message": f"Job description deleted successfully",
            "deleted_id": submission_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting job description: {str(e)}"
        )


# Main endpoint to handle job description submissions
@app.post("/api/submit-job-description", response_model=JobDescriptionResponse)
async def submit_job_description(submission: JobDescriptionSubmission, db: Session = Depends(get_db)):
    """
    Receives a job description from the frontend and saves it to the database.
    
    Args:
        submission: JobDescriptionSubmission object containing the job description
        db: Database session (injected by FastAPI)
        
    Returns:
        JobDescriptionResponse with success status and message
    """
    try:
        # Extract job description and role
        job_desc_str = str(submission.job_description)
        role_str = str(submission.role)
        
        print(f"Received job description: {job_desc_str[:100]}...")
        print(f"Received Role: {role_str}")
        
        # Generate embedding for the job description
        print("Generating embedding...")
        try:
            embedding = generate_job_description_embedding(job_desc_str)
            print(f"Embedding generated successfully (dimension: {len(embedding)})")
        except Exception as embed_error:
            print(f"Warning: Failed to generate embedding: {embed_error}")
            embedding = None
        
        # Find most similar existing job description
        if embedding:
            most_similar_job, similarity_score = find_most_similar_job(embedding, db)
            if most_similar_job:
                print(f"\nMost similar job found:")
                print(f"  ID: {most_similar_job.id}")
                print(f"  Role: {most_similar_job.role}")
                print(f"  Similarity: {similarity_score:.4f} ({similarity_score * 100:.2f}%)")
                print(f"  Job Description: {most_similar_job.job_description[:100]}...")
            else:
                print("No existing jobs with embeddings to compare against")
        
        # Create a new database record with embedding
        db_submission = URLSubmissionModel(
            job_description=job_desc_str, 
            role=role_str,
            embedding=embedding
        )
        
        # Add to database session
        db.add(db_submission)
        
        # Commit the transaction (save to database)
        db.commit()
        
        # Refresh to get the ID and timestamp from the database
        db.refresh(db_submission)
        
        print(f"Saved to database with ID: {db_submission.id}")
        
        # Create a folder in the resumes directory with the record ID
        resumes_dir = Path(__file__).parent.parent / "resumes"
        record_folder = resumes_dir / str(db_submission.id)
        
        try:
            record_folder.mkdir(parents=True, exist_ok=True)
            print(f"Created folder: {record_folder}")
            
            # Compile the appropriate LaTeX template to PDF and save in the folder
            template_compiled = compile_template_to_pdf(role_str, record_folder)
            if template_compiled:
                print(f"Template successfully compiled to PDF for role: {role_str}")
            else:
                print(f"Warning: Failed to compile template to PDF for role: {role_str}")
                
        except Exception as folder_error:
            print(f"Warning: Could not create folder or compile template: {folder_error}")
            # Don't fail the request if folder creation fails
        
        return JobDescriptionResponse(
            success=True,
            message=f"Job description saved successfully to database with ID: {db_submission.id}",
            job_description=job_desc_str
        )
        
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback()
        print(f"Error saving job description: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving job description: {str(e)}")

# Run the server (only when running this file directly)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Allows access from any network interface
        port=8000,        # Backend will run on port 8000
        reload=True       # Auto-reload on code changes (like Vite's HMR)
    )
