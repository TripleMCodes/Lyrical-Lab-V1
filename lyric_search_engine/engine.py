from typing import List, Dict, Tuple, Optional
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import LyricDoc
from .preprocess import normalize
from .storage import SQLiteFeedbackStore

class LLSearchEngine:
    def __init__(
        self,
        feedback_store: Optional[SQLiteFeedbackStore] = None,
        tfidf_max_features: int = 50000,
        tfidf_ngram_range: Tuple[int, int] = (1, 2),
    ):
        self.vectorizer = TfidfVectorizer(
            preprocessor=normalize,
            max_features=tfidf_max_features,
            ngram_range=tfidf_ngram_range,
        )
        self.feedback_store = feedback_store
        self.docs: List[LyricDoc] = []
        self.doc_index: Dict[str, int] = {}
        self.doc_matrix = None

    def index(self, docs: List[LyricDoc]):
        self.docs = docs
        self.doc_index = {d.doc_id: i for i, d in enumerate(docs)}
        texts = [d.title + " " + d.text for d in docs]  # title boost (simple)
        self.doc_matrix = self.vectorizer.fit_transform(texts)
        

    def _tfidf_scores(self, query: str) -> np.ndarray:
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.doc_matrix).flatten()
        # print(sims)
        return sims

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        scores = self._tfidf_scores(query)

        # feedback boost
        if self.feedback_store is not None:
            scores = scores + self._feedback_boost(query)

        top_idx = np.argsort(scores)[::-1][:top_k]
        results = []
        for i in top_idx:
            d = self.docs[i]
            results.append({
                "doc_id": d.doc_id,
                "title": d.title,
                "artist": d.artist,
                "score": float(scores[i]),
            })
        return results

    def _feedback_boost(self, query: str) -> np.ndarray:
        """
        Very simple Phase 1 feedback:
        - sum all feedback values for (query, doc_id)
        - scale it down so it nudges, not dominates
        """
        boost = np.zeros(len(self.docs), dtype=float)
        for q, doc_id, val in self.feedback_store.all():
            if q.strip().lower() == query.strip().lower():
                idx = self.doc_index.get(doc_id)
                if idx is not None:
                    boost[idx] += float(val)

        return 0.15 * boost  # weight controls impact
