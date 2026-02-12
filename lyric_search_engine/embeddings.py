from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingProvider:
    """
    Base interface for embedding providers.
    Lets us swap models later without changing the engine.
    """
    def embed(self, texts: List[str]) -> np.ndarray:
        raise NotImplementedError


class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        vecs = self.model.encode(
            texts,
            normalize_embeddings=True,  # cosine similarity becomes dot product
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return vecs.astype(np.float32)
