import sys
import numpy as np
from database import SessionLocal
from models import URLSubmissionModel
from embeddings import compute_similarity


def compare_job_descriptions(id1: str, id2: str):
    db = SessionLocal()
    
    try:
        job1 = db.query(URLSubmissionModel).filter(URLSubmissionModel.id == id1).first()
        job2 = db.query(URLSubmissionModel).filter(URLSubmissionModel.id == id2).first()
        
        if not job1:
            print(f"Error: Job description with ID {id1} not found")
            return
        
        if not job2:
            print(f"Error: Job description with ID {id2} not found")
            return
        
        if job1.embedding is None:
            print(f"Error: Job 1 (ID: {id1}) has no embedding")
            return
        
        if job2.embedding is None:
            print(f"Error: Job 2 (ID: {id2}) has no embedding")
            return
        
        embedding1 = np.array(job1.embedding)
        embedding2 = np.array(job2.embedding)
        
        similarity = compute_similarity(embedding1, embedding2)
        
        print("\n" + "="*80)
        print("Job Description Similarity Comparison")
        print("="*80)
        
        print(f"\nJob 1:")
        print(f"  ID: {job1.id}")
        print(f"  Role: {job1.role}")
        print(f"  Description: {job1.job_description[:150]}...")
        
        print(f"\nJob 2:")
        print(f"  ID: {job2.id}")
        print(f"  Role: {job2.role}")
        print(f"  Description: {job2.job_description[:150]}...")
        
        print(f"\nCosine Similarity: {similarity:.4f}")
        print(f"Similarity Percentage: {similarity * 100:.2f}%")
        
        if similarity > 0.9:
            print("Assessment: Very Similar")
        elif similarity > 0.7:
            print("Assessment: Similar")
        elif similarity > 0.5:
            print("Assessment: Somewhat Similar")
        else:
            print("Assessment: Different")
        
        print("="*80 + "\n")
        
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_jobs.py <job_id_1> <job_id_2>")
        print("\nExample:")
        print("  python compare_jobs.py 6539a28e-0db6-4e4f-8011-e6a7f2ae9c61 abc123...")
        sys.exit(1)
    
    job_id_1 = sys.argv[1]
    job_id_2 = sys.argv[2]
    
    compare_job_descriptions(job_id_1, job_id_2)
