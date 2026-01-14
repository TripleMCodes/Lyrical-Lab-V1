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
    uid: Optional[int] = None