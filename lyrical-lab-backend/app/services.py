from typing import List

from sqlalchemy.orm import Session
import hashlib

# from lyric_search_engine.models import LyricDoc
from app.lyric_search_engine.models import LyricDoc
# from lyric_search_engine.engine import LLSearchEngine, FieldWeights
from app.lyric_search_engine.engine import LLSearchEngine, FieldWeights
# from lyric_search_engine.storage import SQLiteFeedbackStore
from app.lyric_search_engine.storage import SQLiteFeedbackStore

from app import models


def build_lyric_docs(db: Session, user_id: int) -> List[LyricDoc]:
    """
    Convert DB lyrics into LyricDoc objects.
    Fetches all non-deleted lyrics for a user and converts them to LyricDoc format.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")

    lyrics = (
        db.query(models.Lyrics)
        .filter(models.Lyrics.user_id == user_id)
        .filter(models.Lyrics.deleted_at.is_(None))
        .all()
    )

    docs = []
    for song in lyrics:
        try:
            doc = LyricDoc(
                doc_id=str(song.song_id),
                title=song.song_name,
                text=song.song_lyrics,
                artist=song.song_artist,
                created_at=song.date_created,
                meta={
                    "genre": song.song_genre,
                    "album": song.song_album,
                    "mood": song.song_mood,
                    "version": song.version,
                }
            )
            docs.append(doc)
        except Exception as e:
            print(f"Error converting song {song.song_id} to LyricDoc: {e}")
            continue

    return docs

engine_cache = {}
engine_cache_signatures = {}


def get_engine(user_id: int, db: Session) -> LLSearchEngine:
    """
    Get or create a cached search engine for a user.
    The cache is invalidated if the user's lyrics have changed (by checking a signature).
    
    Args:
        user_id: The user ID to get or create an engine for
        db: Database session
        
    Returns:
        An initialized LLSearchEngine with the user's lyrics indexed
        
    Raises:
        ValueError: If user_id is invalid
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")

    try:
        docs = build_lyric_docs(db, user_id)
        
        # Compute a signature of the current docs
        h = hashlib.sha1()
        for d in docs:
            h.update(f"{d.doc_id}".encode())
        current_sig = h.hexdigest()
        
        # Check if we have a cached engine with the same signature
        if (user_id in engine_cache and 
            user_id in engine_cache_signatures and
            engine_cache_signatures[user_id] == current_sig):
            return engine_cache[user_id]
        
        # Build new engine
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
        
        # Cache it
        engine_cache[user_id] = engine
        engine_cache_signatures[user_id] = current_sig
        
        return engine
        
    except Exception as e:
        raise RuntimeError(f"Failed to initialize search engine for user {user_id}: {e}")


def search_user_lyrics(
    query: str,
    user_id: int,
    db: Session,
    top_k: int = 5,
    with_snippets: bool = True,
) -> List:
    """
    Search user's lyrics with the given query.
    Uses a cached search engine for efficiency.
    
    Args:
        query: The search query string
        user_id: The user ID to search lyrics for
        db: Database session
        top_k: Number of top results to return (1-20)
        with_snippets: Whether to include snippet excerpts in results
        
    Returns:
        A list of search result dictionaries containing doc_id, title, artist, score, and optionally snippet
        
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If search fails
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")
    
    if not isinstance(top_k, int) or top_k < 1 or top_k > 20:
        raise ValueError("top_k must be between 1 and 20")

    try:
        # Use the cached engine
        engine = get_engine(user_id, db)
        
        results = engine.search(
            query,
            top_k=top_k,
            with_snippets=with_snippets,
        )
        
        return results
        
    except Exception as e:
        raise RuntimeError(f"Lyric search failed for user {user_id}: {e}")