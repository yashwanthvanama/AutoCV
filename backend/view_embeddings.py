"""
Script to view embedding data in detail
"""
from database import SessionLocal
from models import URLSubmissionModel
import numpy as np

# Create a database session
db = SessionLocal()

try:
    # Query all URL submissions
    urls = db.query(URLSubmissionModel).order_by(
        URLSubmissionModel.submitted_at.desc()
    ).all()
    
    print(f"\n{'='*80}")
    print(f"Embeddings Analysis - Total records: {len(urls)}")
    print(f"{'='*80}\n")
    
    if urls:
        for i, url in enumerate(urls, 1):
            print(f"\n{'-'*80}")
            print(f"Record #{i}")
            print(f"{'-'*80}")
            print(f"ID: {url.id}")
            print(f"Role: {url.role}")
            print(f"Job Description: {url.job_description[:150]}...")
            print(f"Submitted: {url.submitted_at}")
            
            if url.embedding:
                # Convert to numpy array for analysis
                embedding_array = np.array(url.embedding)
                
                print(f"\n📊 Embedding Statistics:")
                print(f"  - Dimensions: {len(embedding_array)}")
                print(f"  - Data type: {embedding_array.dtype}")
                print(f"  - Min value: {embedding_array.min():.6f}")
                print(f"  - Max value: {embedding_array.max():.6f}")
                print(f"  - Mean value: {embedding_array.mean():.6f}")
                print(f"  - Std deviation: {embedding_array.std():.6f}")
                print(f"  - L2 norm: {np.linalg.norm(embedding_array):.6f}")
                
                print(f"\n🔢 First 10 values:")
                print(f"  {embedding_array[:10]}")
                
                print(f"\n🔢 Last 10 values:")
                print(f"  {embedding_array[-10:]}")
                
                # Check if normalized
                norm = np.linalg.norm(embedding_array)
                is_normalized = abs(norm - 1.0) < 0.01
                print(f"\n✓ Normalized: {'Yes' if is_normalized else 'No'} (L2 norm: {norm:.6f})")
                
            else:
                print(f"\n⚠️  Embedding: Not generated yet")
            
            print()
    else:
        print("No records found in the database.")
        
finally:
    db.close()
    print(f"\n{'='*80}\n")
