from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
from threading import Lock


import os

base_path = Path(__file__).parent
class EmbeddingProvider:
    """
    Base interface for embedding providers.
    """
    def embed(self, texts: List[str]) -> np.ndarray:
        raise NotImplementedError


class SentenceTransformerProvider(EmbeddingProvider):
    pass

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