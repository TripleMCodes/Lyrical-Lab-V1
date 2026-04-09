from typing import Tuple
from .models import LyricDoc

def doc_fields(doc: LyricDoc) -> Tuple[str, str, str]:
    """
    Returns (title_text, chorus_text, verse_text)
    Uses fallbacks if chorus/verses aren't explicitly provided
    """

    title = doc.title or ""
    chorus = doc.chorus or ""
    if doc.verses:
        verses = '\n'.join(doc.verses)
    else:
        # fallback: treat full text as "verses" if not structured
        verses = doc.text or ""
    return title, chorus, verses