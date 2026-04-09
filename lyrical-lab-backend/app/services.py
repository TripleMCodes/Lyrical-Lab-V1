from typing import List

from sqlalchemy.orm import Session

from lyric_search_engine.models import LyricDoc
from lyric_search_engine.engine import LLSearchEngine, FieldWeights
from lyric_search_engine.storage import SQLiteFeedbackStore

import models


def build_lyric_docs(db: Session, user_id: int) -> List[LyricDoc]:
    """
    Convert DB lyrics into LyricDoc objects.
    """

    lyrics = (
        db.query(models.Lyrics)
        .filter(models.Lyrics.user_id == user_id)
        .filter(models.Lyrics.deleted_at.is_(None))
        .all()
    )

    docs = []

    for song in lyrics:
        docs.append(
            LyricDoc(
                str(song.song_id),
                song.song_name,
                song.song_lyrics,
            )
        )

    return docs





def search_user_lyrics(
    query: str,
    user_id: int,
    db: Session,
    top_k: int = 5,
    with_snippets: bool = True,
):
    """
    FastAPI-friendly lyric search.
    """

    docs = build_lyric_docs(db, user_id)

    store = SQLiteFeedbackStore("ll_feedback.db")

    engine = LLSearchEngine(
        feedback_store=store,
        field_weights=FieldWeights(
            title=2.5,
            chorus=2.0,
            verses=1.0,
        ),
    )

    engine.index(docs)

    results = engine.search(
        query,
        top_k=top_k,
        with_snippets=with_snippets,
    )

    return results