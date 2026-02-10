import torch
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np


class EmbeddingGenerator:
    
    def __init__(self, model_name: str = "nomic-ai/nomic-embed-text-v1.5"):
        print(f"Loading model: {model_name}")
        
        if torch.backends.mps.is_available():
            device = 'mps'
        elif torch.cuda.is_available():
            device = 'cuda'
        else:
            device = 'cpu'
            
        self.model = SentenceTransformer(
            model_name,
            trust_remote_code=True,
            device=device
        )
        self.device = device
        print(f"Model loaded on device: {self.device}")
        
    def generate_embedding(
        self, 
        text: str, 
        task_prefix: str = "clustering"
    ) -> np.ndarray:
        prefixed_text = f"{task_prefix}: {text}"
        
        embedding = self.model.encode(
            prefixed_text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        return embedding
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        return float(np.dot(embedding1, embedding2))


_embedding_generator: Optional[EmbeddingGenerator] = None


def get_embedding_generator() -> EmbeddingGenerator:
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator


def generate_job_description_embedding(job_description: str) -> List[float]:
    generator = get_embedding_generator()
    embedding = generator.generate_embedding(job_description, task_prefix="clustering")
    return embedding.tolist()


if __name__ == "__main__":
    print("Testing Embedding Generator")
    print("=" * 80)
    
    test_text = "We are looking for a Senior Software Engineer with expertise in Python and machine learning."
    
    generator = get_embedding_generator()
    embedding = generator.generate_embedding(test_text, task_prefix="clustering")
    
    print(f"\nTest text: {test_text}")
    print(f"\nEmbedding shape: {embedding.shape}")
    print(f"Embedding dtype: {embedding.dtype}")
    print(f"L2 norm: {np.linalg.norm(embedding):.6f}")
    print(f"\nFirst 10 values: {embedding[:10]}")
    print(f"Last 10 values: {embedding[-10:]}")
    
    test_text2 = "Senior Python developer needed for AI/ML projects."
    embedding2 = generator.generate_embedding(test_text2, task_prefix="clustering")
    similarity = generator.compute_similarity(embedding, embedding2)
    
    print(f"\n\nSimilarity test:")
    print(f"Text 1: {test_text}")
    print(f"Text 2: {test_text2}")
    print(f"Cosine Similarity: {similarity:.4f}")
    print("\n" + "=" * 80)
