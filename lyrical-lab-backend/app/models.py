from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, func, UniqueConstraint
)
import uuid

class Users(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(150), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    date_created = Column(DateTime, nullable=False, default=func.now())

    lyrics = relationship("Lyrics", back_populates="user", cascade="all, delete-orphan")

    scratchpad = relationship(
        "Scratchpad",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Lyrics(Base):
    __tablename__ = "lyrics"
    __table_args__ = (
        UniqueConstraint("user_id", "client_uid", name="uq_lyrics_user_client_uid"),
    )

    # Cloud ID
    song_id = Column(Integer, primary_key=True, autoincrement=True)

    # Ownership (cloud truth)
    user_id = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)

    # Idempotency / client linkage (desktop-local song id)
    client_uid = Column(String(36), nullable=True, index=True)
    source = Column(String(20), nullable=False, server_default="web")  # "desktop" | "web"

    # Metadata
    song_name = Column(String(150), nullable=False)
    song_artist = Column(String(150), nullable=False)
    song_album = Column(String(100), nullable=True)
    song_genre = Column(String(100), nullable=False)
    song_mood = Column(String(100), nullable=True)

    # Content
    song_lyrics = Column(Text, nullable=False)

    # Timestamps
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Optional soft delete
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("Users", back_populates="lyrics")

    
class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False, index=True)

    total_writing_time = Column(Integer, nullable=False, default=0)
    writing_sessions = Column(Integer, nullable=False, default=0)

    date_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


class Scratchpad(Base):
    __tablename__ = "scratchpad"

    id = Column(Integer, primary_key=True, autoincrement=True)

    note = Column(Text, nullable=False)

    date_created = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    date_modified = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    user_id = Column(
        Integer,
        ForeignKey("users.uid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user = relationship("Users", back_populates="scratchpad")

class StateFold(Base):
    __tablename__ = "statefold"

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_name = Column(String(150), nullable=True)
    song_genre = Column(String(150), nullable=True)
    song_lyrics = Column(Text, nullable=True)
    song_artist = Column(String(150), nullable=True)
    song_mood = Column(String(150), nullable=True)
    song_album = Column(String(150), nullable=True)
    user_id = Column(Integer, ForeignKey('users.uid'), nullable=False, unique=True)

class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
