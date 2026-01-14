from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import engine, get_db
from .. import models, schemas, utils, oauth2
import logging
logging.basicConfig(level=logging.DEBUG)

oauth2.SECRET_KEY

router = APIRouter(tags=['Authentication'])

@router.post('/api/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    # logging.debug(f'The user info is {user.uid} {type(user.id)}')

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid credentials'
        )
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    #create a token
    access_token = oauth2.create_access_token(data = {'uid': int(user.uid)})
    refresh_token = oauth2.create_refresh_token({"uid": int(user.uid)})

    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
        }


@router.post("/refresh")
def refresh_token(token: str = Depends(oauth2.oauth2_scheme)):
    try:
        payload = jwt.decode(token, oauth2.SECRET_KEY, algorithms=[oauth2.ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401)

        uid = payload.get("uid")
        if uid is None:
            raise HTTPException(status_code=401)

        new_access_token = oauth2.create_access_token({"uid": uid})
        return {"access_token": new_access_token}

    except JWTError:
        raise HTTPException(status_code=401)