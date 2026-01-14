from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    artist_name: str
    age: int
    password: str
    email: EmailStr

class UserOut(BaseModel):
    uid: int
    artist_name: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    uid: int

class NewSong(BaseModel):
    song_name: str
    song_artist: str
    song_lyrics: str
    song_mood: Optional[str] = None
    song_genre: Optional[str] = None
    song_album: Optional[str] = None