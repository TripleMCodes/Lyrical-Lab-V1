from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Users(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(150), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    date_created = Column(DateTime, nullable=False, default=func.now())

    lyrics = relationship("Lyrics", back_populates="user", cascade="all, delete-orphan")

class Lyrics(Base):
    __tablename__ = "lyrics"

    song_id = Column(Integer, primary_key=True, autoincrement=True)
    song_name = Column(String(150), nullable=False)
    song_genre = Column(String(100), nullable=False)
    song_lyrics = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.uid'), nullable=False)
    song_artist = Column(String(150), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_modified = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    song_mood = Column(String(100), nullable=True)
    song_album = Column(String(100), nullable=True)

    user = relationship("Users", back_populates="lyrics")


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
