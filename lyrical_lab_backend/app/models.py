from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, func, UniqueConstraint, Index, UUID, Boolean
)
import uuid

class Users(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(150), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    blocked = Column(Boolean, nullable=False, server_default='false')
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
        # Idempotent uploads: a given user + client_uid points to exactly one cloud song
        UniqueConstraint("user_id", "client_uid", name="uq_lyrics_user_client_uid"),
    )

    # Cloud ID
    song_id = Column(Integer, primary_key=True, autoincrement=True)

    # Ownership (cloud truth)
    user_id = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)

    # Idempotency / client linkage (stable UUID generated on client per local song)
    # Postgres-native UUID is better than String(36)
    client_uid = Column(UUID(as_uuid=True), nullable=True, index=True)

    # Origin (helps analytics/debug)
    source = Column(String(20), nullable=False, server_default="web")  # "desktop" | "web"

    # Metadata (kept on HEAD only; versions track lyrics text only)
    song_name = Column(String(150), nullable=False)
    song_artist = Column(String(150), nullable=False)
    song_album = Column(String(100), nullable=True)
    song_genre = Column(String(100), nullable=False)
    song_mood = Column(String(100), nullable=True)

    # Content (HEAD)
    song_lyrics = Column(Text, nullable=False)

    # Versioning (NEW)
    # - version: current HEAD version number
    # - lyrics_hash: sha256 hex (64 chars) of *normalized* lyrics
    # - hash_algo: stored for future-proofing; default sha256
    version = Column(Integer, nullable=False, server_default="1")
    lyrics_hash = Column(String(64), nullable=False)
    hash_algo = Column(String(20), nullable=False, server_default="sha256")

    # Timestamps (use tz-aware for Postgres)
    date_created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    date_modified = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Optional soft delete
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("Users", back_populates="lyrics")

    versions = relationship(
        "LyricsVersion",
        back_populates="head",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="LyricsVersion.version.desc()",
    )



class LyricsVersion(Base):
    __tablename__ = "lyrics_versions"
    __table_args__ = (
        UniqueConstraint("lyrics_id", "version", name="uq_lyrics_versions_lyrics_id_version"),
        Index("ix_lyrics_versions_lyrics_id_created_at", "lyrics_id", "created_at"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Which "head" song this snapshot belongs to
    lyrics_id = Column(Integer, ForeignKey("lyrics.song_id", ondelete="CASCADE"), nullable=False)

    # Snapshot number (stores the *old* version number you are archiving)
    version = Column(Integer, nullable=False)

    # The snapshot text
    lyrics = Column(Text, nullable=False)

    # Hash of this snapshot (sha256 of normalized lyrics)
    lyrics_hash = Column(String(64), nullable=False)  # sha256 hex = 64 chars
    hash_algo = Column(String(20), nullable=False, server_default="sha256")

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Optional: why this snapshot was created (manual save, autosave, before upload, etc.)
    note = Column(String(120), nullable=True)

    # Relationship back to head
    head = relationship("Lyrics", back_populates="versions")
    
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
    api_key = Column(String(255), nullable=True)
    api_url = Column(String(255), nullable=True)


class APIRequestLimit(Base):
    __tablename__ = "api_request_limits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False, index=True)
    
    # Track requests per day
    request_count = Column(Integer, nullable=False, default=0)
    date_created = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)


class ContactMessages(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    date_created = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)


song = {'user_id': 1, 'client_uid': '345c10a7-f2ab-4c8a-a9c1-231173a8a3b8', 'source': 'desktop', 'song_artist': 'MMMC', 'song_genre': 'Pop', 'song_lyrics': "8 pre-chorus + chorus\n\n16 verse\n\n8 pre-chorus + chorus\n\n16 verse\n\n8 pre-chorus + prechorus\n\nSong: Borrowed Time\n\nIntro:\nMy mind is racing//\nDreams I'm chasing//\nstuck in my horrors and/\nFear builds cages//\n\nPain writes lyrics//\nBut it is costly I pay with interest//\n\nChorus:\nTimes flies/\nsee the feathers on the hands of time//\nIt's a flight risk/\nbut I'll take it, it's all I got//\n\nVerse 1:\nHow my life's spent/\nin my life span//(1)\nis with my hopes up/\nand my head up/\nand my hands up//(1)\ntrynna far-span/\nbut I ain't really that deep/ \nand life is a bitch/\n I've been forspanned//(2)\n[4]\n\nWas an angel/\nI got twisted/\nChanged the angle/\nLost my wing span//(2)\nTime is money and life is an expense//(1)\nI don't trust it, it's a sus Pense//(1)\n[4]\n\nI gotta repeat this is intense//(1)\nLife is movies and I hate pretence love the suspense//(1.5)\nNo nostalgia cause the past's tense//(1)\nI've made it here hope I past tense//(1)\n[4]\n\nIs my fearing in the past tense?//(1)\nI hope that it is said/(.5)\nLike a convict I hoped that it is sentenced//(1)\nThat being said/(.5)\nI'm swimming in a lot blood//(1)\n[4]\n\nMe my self and I in a pool of death//(1)\nfeel the push of life and the pull of death//(1)\nLooking for some depth/\ntrynna make a splash/ \nfrom pool of thoughts//(2)\n[4]\nBut drowning in a lot of debt//(1)\n\nSo I pay the price//(.5)\nBut don't get it twisted I ain't living on borrowed money//(1.5)\nI'm just living on borrowed time//(1)\n\nChorus:\nTimes flies/\nsee the feathers on the hands of time//\nIt's a flight risk/\nbut I'll take it, it's all I got//\n\nVerse 2:\nAll that's in the dark shall come to light, and so you better put your money where your mouth is//(2)\nTime passes and we are passer-bys, and we really spend our lives trying to rebuy it//(2)\n[4]\n\nIf as above so below//(1)\nIs forward just as backwards I wanna know//(1)\n\nLife writes stories and time buries moments//(1)\nlive by coping and die being hopeless//(1)\nhope is dying and coping by living//(1)\nmoments bury time and stories write life//(1)\n\nthougth father is a loan shark I owe it to me to spend my time and spend my life//2\nI assume after all it is not borrowed time when I pay no mind//(2)\n\nChorus:\nTimes flies/\nsee the feathers on the hands of time//\nIt's a flight risk/\nbut I'll take it, it's all I got//\n\nOutro:\nRacing my mind 'n'/\nChased by my nightmares/\nStuck in my horrors/\nCages build Fears/\n\nLyrics write pain//\nI pay with interest, cause it is costly//\n\n\n\n\n\n\n\n\nDon't get it twisted, I ain't living on borrowed money, I'm just living on borrowed time//\nLife writes stories and time buries moments//\nlive by coping and die being hopeless//\nhope is dying and coping by living//\nmoments bury time and stories write life//\n\n\nMoments bury time and life writes stories//\nhope is for the weak\nhope eases the weak\n\n\nLearning from mistakes and ignorant for successes\n\nBurning dires got me burning bridge for money to burn//\nSay I'm rich in mind no penny for my thoughts, cause I'm thinking millions\n\nTime is money\nlife savings \nsaving lifes\n\nfrom heart of stone to heart of cold, that's alchemy\nIn my element, from lot of bonds to fewer bonds, that's chemistry//\n\ntime flow is a cash flow\nDays of our lifes spent in days of our lives", 'lyrics_hash': '5c871be5c295fd9eabb5f54e3a37f4c749ece0a8e2234b2a50032498e93b0cd0', 'date_created': '2026-03-19T11:24:49.648910+02:00', 'deleted_at': None, 'song_id': 20, 'song_name': 'Borrowed time', 'song_album': None, 'song_mood': None, 'version': 1, 'hash_algo': 'sha256', 'date_modified': '2026-03-19T11:24:49.648910+02:00'}