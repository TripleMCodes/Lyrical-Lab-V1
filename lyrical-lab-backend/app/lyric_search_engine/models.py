from dataclasses import dataclass
from  datetime import datetime
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class LyricDoc:
    doc_id: str
    title: str
    text: str
    artist: Optional[str] = None
    chorus: Optional[str] = None
    verses: Optional[str] = None
    created_at: Optional[datetime] = None
    meta: Optional[Dict[str, Any]] = None