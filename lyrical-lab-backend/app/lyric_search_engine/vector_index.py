from __future__ import annotations
from typing import List, Tuple
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

class FaissIndex:
    def __init__(self, dim: int):
        if faiss is None:
            raise RuntimeError("FAISS not installed. Try: pip install faiss-cpu")
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  
        self.doc_ids: List[str] = []

    def build(self, doc_ids: List[str], vectors: np.ndarray) -> None:
        assert vectors.dtype == np.float32
        assert vectors.shape[1] == self.dim
        self.index.reset()
        self.index.add(vectors)
        self.doc_ids = list(doc_ids)

    def search(self, query_vec: np.ndarray, top_k: int = 10) -> List[Tuple[str, float]]:
        q = query_vec.astype(np.float32)
        if q.ndim == 1:
            q = q.reshape(1, -1)
        scores, idxs = self.index.search(q, top_k)
        results = []
        for i, s in zip(idxs[0], scores[0]):
            if i == -1:
                continue
            results.append((self.doc_ids[int(i)], float(s)))
        return results
