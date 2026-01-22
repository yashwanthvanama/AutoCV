"""
Quick script to check what's in the database
"""
from database import SessionLocal
from models import URLSubmissionModel

# Create a database session
db = SessionLocal()

try:
    # Query all URL submissions
    urls = db.query(URLSubmissionModel).order_by(
        URLSubmissionModel.submitted_at.desc()
    ).all()
    
    print(f"\n{'='*60}")
    print(f"Total URLs in database: {len(urls)}")
    print(f"{'='*60}\n")
    
    if urls:
        for i, url in enumerate(urls, 1):
            print(f"{i}. URL: {url.url}")
            print(f"   ID: {url.id}")
            print(f"   Submitted at: {url.submitted_at}")
            print()
    else:
        print("No URLs found in the database yet.")
        print("Submit a URL through the frontend to see it here!\n")
        
finally:
    db.close()
