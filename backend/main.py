from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
import uvicorn

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

# Main endpoint to handle URL submissions
@app.post("/api/submit-url", response_model=URLResponse)
async def submit_url(submission: URLSubmission):
    """
    Receives a URL from the frontend and processes it.
    
    Args:
        submission: URLSubmission object containing the URL
        
    Returns:
        URLResponse with success status and message
    """
    try:
        # Convert the URL to a string for processing
        url_str = str(submission.url)
        
        # Here you can add your custom logic to process the URL
        # For example:
        # - Store it in a database
        # - Scrape the website
        # - Generate a CV from LinkedIn profile
        # - etc.
        
        print(f"Received URL: {url_str}")
        
        # For now, we'll just return a success response
        return URLResponse(
            success=True,
            message="URL received and processed successfully",
            url=url_str
        )
        
    except Exception as e:
        # If something goes wrong, raise an HTTP exception
        raise HTTPException(status_code=500, detail=str(e))

# Run the server (only when running this file directly)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Allows access from any network interface
        port=8000,        # Backend will run on port 8000
        reload=True       # Auto-reload on code changes (like Vite's HMR)
    )
