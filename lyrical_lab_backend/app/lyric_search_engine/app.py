from __future__ import annotations

from typing import List, Dict, Any

from lyric_search_engine.models import LyricDoc
from lyric_search_engine.engine import LLSearchEngine, FieldWeights
from lyric_search_engine.storage import SQLiteFeedbackStore


def build_engine(docs: List[LyricDoc]) -> LLSearchEngine:
    """
    Builds and indexes the lyric search engine.
    """
    store = SQLiteFeedbackStore("ll_feedback.db")

    engine = LLSearchEngine(
        feedback_store=store,
        field_weights=FieldWeights(
            title=2.5,
            chorus=2.0,
            verses=1.0
        ),
    )

    engine.index(docs)

    return engine


def search_lyrics(
    query: str,
    docs: List[LyricDoc],
    top_k: int = 5,
    with_snippets: bool = True
) -> List[Dict[str, Any]]:
    """
    API-friendly lyric search function.

    Returns JSON-friendly results.
    """

    engine = build_engine(docs)

    results = engine.search(
        query,
        top_k=top_k,
        with_snippets=with_snippets
    )

    return results