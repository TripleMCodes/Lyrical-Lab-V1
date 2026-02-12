from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import hashlib

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import LyricDoc
from .preprocess import normalize
from .storage import SQLiteFeedbackStore
from .stopwords import DEFAULT_STOPWORDS
from .fields import doc_fields
from .embeddings import EmbeddingProvider, SentenceTransformerProvider
from .vector_index import FaissIndex


@dataclass
class FieldWeights:
    title: float = 2.5
    chorus: float = 1.8
    verses: float = 1.0

@dataclass
class HybridWeights:
    tfidf: float = 0.4
    semantic: float = 0.6


class LLSearchEngine:
    
    def __init__(
        self,
        feedback_store: Optional[SQLiteFeedbackStore] = None,
        tfidf_max_features: int = 50000,
        tfidf_ngram_range: Tuple[int, int] = (1, 2),
        stopwords: Optional[set[str]] = None,
        field_weights: Optional[FieldWeights] = None,

        embedding_provider: Optional[EmbeddingProvider] = None,
        hybrid_weights: Optional[HybridWeights] = None,
        semantic_top_k: int = 50,  # candidates pulled from semantic index before rerank
    ):
        sw = stopwords if stopwords is not None else DEFAULT_STOPWORDS

        self.vectorizer = TfidfVectorizer(
            preprocessor=normalize,
            max_features=tfidf_max_features,
            ngram_range=tfidf_ngram_range,
            stop_words=sorted(list(sw)),
        )

        self.feedback_store = feedback_store
        self.field_weights = field_weights or FieldWeights()

        self.embedding_provider = embedding_provider or SentenceTransformerProvider()
        self.hybrid_weights = hybrid_weights or HybridWeights()
        self.semantic_top_k = semantic_top_k

        self.docs: List[LyricDoc] = []
        self.doc_index: Dict[str, int] = {}

        # Cached TF-IDF matrices
        self._title_matrix = None
        self._chorus_matrix = None
        self._verses_matrix = None

        # Cached semantic index
        self._semantic_index: Optional[FaissIndex] = None
        self._semantic_dim: Optional[int] = None

        # caching signature
        self._signature: Optional[str] = None

    # caching helpers
    def _compute_signature(self, docs: List[LyricDoc]) -> str:
        """
        Hash doc_id + relevant fields. If this hash doesn't change, we don't rebuild matrices.
        """
        h = hashlib.sha1()
        for d in docs:
            title, chorus, verses = doc_fields(d)
            payload = f"{d.doc_id}|{title}|{chorus}|{verses}".encode("utf-8", errors="ignore")
            h.update(payload)
            h.update(b"\n---\n")
        return h.hexdigest()

    def index(self, docs: List[LyricDoc], force: bool = False) -> bool:
        """
        Returns True if index was rebuilt, False if cached index reused.
        """
        sig = self._compute_signature(docs)
        if (not force) and (self._signature == sig) and (self._title_matrix is not None):
            # Nothing changed: keep cached matrices
            self.docs = docs
            self.doc_index = {d.doc_id: i for i, d in enumerate(docs)}
            return False

        self.docs = docs
        self.doc_index = {d.doc_id: i for i, d in enumerate(docs)}

        titles, choruses, verses = [], [], []
        for d in docs:
            t, c, v = doc_fields(d)
            titles.append(t)
            choruses.append(c)
            verses.append(v)

        # Fit vocab on ALL text (so all field transforms share the same vocabulary)
        fit_corpus = [
            f"{titles[i]} {choruses[i]} {verses[i]}"
            for i in range(len(docs))
        ]
        self.vectorizer.fit(fit_corpus)

        self._title_matrix = self.vectorizer.transform(titles)
        self._chorus_matrix = self.vectorizer.transform(choruses)
        self._verses_matrix = self.vectorizer.transform(verses)

        semantic_texts = [
            f"{titles[i]}\n{choruses[i]}\n{verses[i]}".strip()
            for i in range(len(docs))
        ]

        doc_ids = [d.doc_id for d in docs]
        vectors = self.embedding_provider.embed(semantic_texts)  # shape (n, dim), float32, normalized

        self._semantic_dim = int(vectors.shape[1])
        self._semantic_index = FaissIndex(self._semantic_dim)
        self._semantic_index.build(doc_ids, vectors)

        self._signature = sig
        return True

    # --------- scoring ---------
    def _field_scores(self, query: str) -> np.ndarray:
        qv = self.vectorizer.transform([query])

        wt = self.field_weights
        title_s = cosine_similarity(qv, self._title_matrix).flatten()
        chorus_s = cosine_similarity(qv, self._chorus_matrix).flatten()
        verses_s = cosine_similarity(qv, self._verses_matrix).flatten()

        # weighted sum
        return (wt.title * title_s) + (wt.chorus * chorus_s) + (wt.verses * verses_s)

    def _feedback_boost(self, query: str) -> np.ndarray:
        """
        Same-query feedback boost (Phase 1).
        """
        if self.feedback_store is None:
            return np.zeros(len(self.docs), dtype=float)

        boost = np.zeros(len(self.docs), dtype=float)
        q_norm = query.strip().lower()

        for q, doc_id, val in self.feedback_store.all():
            if q.strip().lower() == q_norm:
                idx = self.doc_index.get(doc_id)
                if idx is not None:
                    boost[idx] += float(val)

        return 0.15 * boost

    # snippet extraction
    def _best_line_snippet(self, query: str, doc: LyricDoc, max_len: int = 120) -> str:
        """
        Find the best matching line in doc.text using TF-IDF cosine similarity.
        Only used for top results (cheap enough).
        """
        lines = [ln.strip() for ln in (doc.text or "").splitlines() if ln.strip()]
        if not lines:
            return ""

        qv = self.vectorizer.transform([query])
        line_matrix = self.vectorizer.transform(lines)
        sims = cosine_similarity(qv, line_matrix).flatten()
        best_i = int(np.argmax(sims))
        snippet = lines[best_i]

        if len(snippet) > max_len:
            snippet = snippet[: max_len - 1] + "…"
        return snippet

    # public search
    def search(self, query: str, top_k: int = 10, with_snippets: bool = True) -> List[Dict]:
        if self._title_matrix is None:
            raise RuntimeError("Index is empty. Call engine.index(docs) first.")

        tfidf_scores = self._field_scores(query)
        sem_scores = self._semantic_scores(query)

        hw = self.hybrid_weights
        scores = (hw.tfidf * tfidf_scores) + (hw.semantic * sem_scores)

        if self.feedback_store is not None:
            scores = scores + self._feedback_boost(query)

        top_idx = np.argsort(scores)[::-1][:top_k]

        results = []
        for i in top_idx:
            d = self.docs[int(i)]
            item = {
                "doc_id": d.doc_id,
                "title": d.title,
                "artist": d.artist,
                "score": float(scores[int(i)]),
            }
            if with_snippets:
                item["snippet"] = self._best_line_snippet(query, d)
            results.append(item)

        return results


    def _semantic_scores(self, query: str) -> np.ndarray:
        """
        Returns an array aligned to docs, where each entry is the semantic similarity.
        Uses FAISS for top candidate retrieval, then expands into a full score vector.
        """
        if self._semantic_index is None:
            return np.zeros(len(self.docs), dtype=float)

        qvec = self.embedding_provider.embed([query])[0]  # (dim,)
        candidates = self._semantic_index.search(qvec, top_k=self.semantic_top_k)

        scores = np.zeros(len(self.docs), dtype=float)
        for doc_id, sim in candidates:
            idx = self.doc_index.get(doc_id)
            if idx is not None:
                scores[idx] = float(sim)
        return scores

