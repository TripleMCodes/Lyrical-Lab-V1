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


@router.post('/api/admin/login', response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    admin = db.query(models.Admin).filter(models.Admin.admin_name == admin_credentials.username).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid admin credentials'
        )
    
    if not utils.verify(admin_credentials.password, admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid admin credentials')
    
    #create a token
    access_token = oauth2.create_access_token(data = {'admin_id': int(admin.admin_id)})
    refresh_token = oauth2.create_refresh_token({"admin_id": int(admin.admin_id)})

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
        admin_id = payload.get("admin_id")
        if uid is None and admin_id is None:
            raise HTTPException(status_code=401)

        data = {}
        if uid:
            data["uid"] = uid
        if admin_id:
            data["admin_id"] = admin_id

        new_access_token = oauth2.create_access_token(data)
        return {"access_token": new_access_token}

    except JWTError:
        raise HTTPException(status_code=401)