from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    artist_name: str
    age: int
    password: str
    email: EmailStr

class UserOut(BaseModel):
    uid: int
    artist_name: str
    email: EmailStr
    blocked: bool

class AdminNameUpdate(BaseModel):
    admin_name: str

class AdminPasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class AdminApiUpdate(BaseModel):
    api_key: Optional[str] = None
    api_url: Optional[str] = None

class UserPasswordUpdate(BaseModel):
    new_password: str

class UserBlockUpdate(BaseModel):
    blocked: bool

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    uid: Optional[int] = None
    admin_id: Optional[int] = None

class NewSong(BaseModel):
    song_id: Optional[int] = None
    song_name: str
    song_artist: str
    song_lyrics: str
    song_mood: Optional[str] = None
    song_genre: Optional[str] = None
    song_album: Optional[str] = None

class AdminLyricOut(BaseModel):
    song_id: int
    song_name: str
    song_artist: str
    song_lyrics: str
    user_name: str
    date_created: datetime

    class Config:
        from_attributes = True
    
