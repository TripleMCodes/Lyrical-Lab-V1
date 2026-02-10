import sqlite3
from typing import Iterable, Tuple

class SQLiteFeedbackStore:
    def __init__(self, path: str):
        self.path = path
        self._init()

    def _conn(self):
        return sqlite3.connect(self.path)

    def _init(self):
        with self._conn() as con:
            con.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                doc_id TEXT NOT NULL,
                value REAL NOT NULL,
                ts DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            con.commit()

    def add(self, query: str, doc_id: str, value: float):
        with self._conn() as con:
            con.execute(
                "INSERT INTO feedback(query, doc_id, value) VALUES (?, ?, ?)",
                (query, doc_id, float(value))
            )
            con.commit()

    def all(self) -> Iterable[Tuple[str, str, float]]:
        with self._conn() as con:
            cur = con.execute("SELECT query, doc_id, value FROM feedback")
            yield from cur.fetchall()

    def clear(self):
        with self._conn() as con:
            con.execute("DELETE FROM feedback")
            con.commit()
