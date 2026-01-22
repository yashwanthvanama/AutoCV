from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from typing import Optional
import uvicorn

# Import database components
from database import get_db, engine, Base
from models import URLSubmissionModel

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
class URLSubmission(BaseModel):
    url: HttpUrl  # Automatically validates that it's a proper URL
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com"
            }
        }

# Response model
class URLResponse(BaseModel):
    success: bool
    message: str
    url: str
    
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


# Endpoint to get all submitted URLs (for testing/debugging)
@app.get("/api/urls")
async def get_all_urls(db: Session = Depends(get_db)):
    """
    Retrieve all URLs from the database.
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        List of all submitted URLs
    """
    try:
        urls = db.query(URLSubmissionModel).order_by(
            URLSubmissionModel.submitted_at.desc()
        ).all()
        
        return {
            "success": True,
            "count": len(urls),
            "urls": [
                {
                    "id": str(url.id),
                    "url": url.url,
                    "submitted_at": url.submitted_at.isoformat()
                }
                for url in urls
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving URLs: {str(e)}"
        )


# Main endpoint to handle URL submissions
@app.post("/api/submit-url", response_model=URLResponse)
async def submit_url(submission: URLSubmission, db: Session = Depends(get_db)):
    """
    Receives a URL from the frontend and saves it to the database.
    
    Args:
        submission: URLSubmission object containing the URL
        db: Database session (injected by FastAPI)
        
    Returns:
        URLResponse with success status and message
    """
    try:
        # Convert the URL to a string
        url_str = str(submission.url)
        
        print(f"Received URL: {url_str}")
        
        # Create a new database record
        db_submission = URLSubmissionModel(url=url_str)
        
        # Add to database session
        db.add(db_submission)
        
        # Commit the transaction (save to database)
        db.commit()
        
        # Refresh to get the ID and timestamp from the database
        db.refresh(db_submission)
        
        print(f"Saved to database with ID: {db_submission.id}")
        
        return URLResponse(
            success=True,
            message=f"URL saved successfully to database with ID: {db_submission.id}",
            url=url_str
        )
        
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback()
        print(f"Error saving URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving URL: {str(e)}")

# Run the server (only when running this file directly)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Allows access from any network interface
        port=8000,        # Backend will run on port 8000
        reload=True       # Auto-reload on code changes (like Vite's HMR)
    )
