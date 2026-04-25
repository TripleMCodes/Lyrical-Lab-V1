from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
from threading import Lock
import os

base_path = Path(__file__).parent

# Module-level singleton embedding provider (lazy-loaded on first use)
_embedding_provider_instance = None
_embedding_provider_lock = Lock()


def get_embedding_provider(model_path: str = None) -> "SentenceTransformerProvider":
    """
    Get or create the global embedding provider instance.
    Ensures only one model is loaded in memory across the entire app.
    
    Args:
        model_path: Path to the model directory (defaults to bundled model)
        
    Returns:
        The singleton SentenceTransformerProvider instance
    """
    global _embedding_provider_instance
    
    if _embedding_provider_instance is not None:
        return _embedding_provider_instance
    
    with _embedding_provider_lock:
        if _embedding_provider_instance is None:
            if model_path is None:
                model_path = base_path / "models/all-MiniLM-L6-v2"
            _embedding_provider_instance = SentenceTransformerProvider(model_path)
    
    return _embedding_provider_instance


class EmbeddingProvider:
    """
    Base interface for embedding providers.
    """
    def embed(self, texts: List[str]) -> np.ndarray:
        raise NotImplementedError


class SentenceTransformerProvider(EmbeddingProvider):

    _model = None  # shared singleton
    _model_lock = Lock()

    def __init__(self, model_path: str = base_path / "models/all-MiniLM-L6-v2"):

        os.environ["TRANSFORMERS_OFFLINE"] = "1"

        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Make sure it is bundled with the app."
            )

        with SentenceTransformerProvider._model_lock:
            if SentenceTransformerProvider._model is None:
                SentenceTransformerProvider._model = SentenceTransformer(str(model_path))

        self.model = SentenceTransformerProvider._model

    def embed(self, texts: List[str]) -> np.ndarray:

        vecs = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return vecs.astype(np.float32)