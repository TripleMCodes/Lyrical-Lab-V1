from fastapi import APIRouter, Depends, Query, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import engine, get_db
from .. import models, schemas, utils, oauth2
from typing import Optional
import logging
logging.basicConfig(level=logging.DEBUG)

oauth2.SECRET_KEY

router = APIRouter(tags=['Authentication'])

@router.post('/api/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    logging.debug(f"logging user")
    
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    # logging.debug(f'The user info is {user.uid} {type(user.id)}')

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid credentials'
        )
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    if user.blocked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Account is blocked')
    
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

    logging.debug(f"logging in admin")
    
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

@router.patch('/api/admin/settings/name')
def admin_change_name(
    payload: schemas.AdminNameUpdate,
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    existing = db.query(models.Admin).filter(models.Admin.admin_name == payload.admin_name).first()
    if existing and existing.admin_id != current_admin.admin_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Admin name is already taken.')

    current_admin.admin_name = payload.admin_name
    db.commit()
    db.refresh(current_admin)
    return {"message": "Admin name updated successfully."}

@router.patch('/api/admin/settings/password')
def admin_change_password(
    payload: schemas.AdminPasswordUpdate,
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    if not utils.verify(payload.current_password, current_admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Current password is incorrect.')

    current_admin.password = utils.hash(payload.new_password)
    db.commit()
    return {"message": "Admin password updated successfully."}

@router.patch('/api/admin/settings/api')
def admin_change_api(
    payload: schemas.AdminApiUpdate,
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    if payload.api_key is not None:
        current_admin.api_key = payload.api_key
    if payload.api_url is not None:
        current_admin.api_url = payload.api_url

    db.commit()
    return {"message": "Admin API settings updated successfully."}

@router.get('/api/admin/users', response_model=list[schemas.UserOut])
def admin_list_users(
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    data = db.query(models.Users).all()
    print(data)
    return data

@router.patch('/api/admin/users/{user_id}/password')
def admin_change_user_password(
    user_id: int,
    payload: schemas.UserPasswordUpdate,
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    user = db.query(models.Users).filter(models.Users.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    user.password = utils.hash(payload.new_password)
    db.commit()
    return {"message": "User password updated successfully."}


@router.patch('/api/admin/block/user/{user_id}')
def admin_block_user(
    data: dict,
    user_id: int,
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    user = db.query(models.Users).filter(models.Users.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    user.blocked = data['blocked']
    db.commit()
    return {"message": "User has been blocked successfully."}

@router.get('/api/admin/songs', response_model=list[schemas.AdminLyricOut])
def admin_list_songs(
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(4, ge=1, le=100),
):
    
    
    lyrics = db.query(
        models.Lyrics.song_id,
        models.Lyrics.song_name,
        models.Lyrics.song_artist,
        models.Lyrics.song_lyrics,
        models.Lyrics.date_created,
        models.Users.artist_name.label('user_name')
    ).join(models.Users, models.Lyrics.user_id == models.Users.uid).all()

    # print(lyrics)

    # return [schemas.AdminLyricOut(**dict(row)) for row in lyrics]
    return lyrics

@router.get("/api/admin/messages")
def admin_get_messages(
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    from sqlalchemy import func
    
    total = db.query(func.count(models.Message.id)).scalar() or 0
    
    messages = db.query(models.Message).order_by(
        models.Message.date_created.desc()
    ).offset((page - 1) * size).limit(size).all()
    
    pages = (total + size - 1) // size if size else 1
    
    return {
        "items": messages,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "next_page": page + 1 if page < pages else None,
        "prev_page": page - 1 if page > 1 else None,
    }

@router.delete("/api/admin/messages/{message_id}")
def admin_delete_message(
    message_id: int,
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Message not found.')
    
    db.delete(message)
    db.commit()
    return {"message": "Message deleted successfully."}

@router.delete('/api/admin/songs/{song_id}')
def admin_delete_song(
    song_id: int,
    current_admin: models.Admin = Depends(oauth2.get_current_admin),
    db: Session = Depends(get_db),
):
    song = db.query(models.Lyrics).filter(models.Lyrics.song_id == song_id).first()
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found.')

    db.delete(song)
    db.commit()
    return {"message": "Song deleted successfully."}


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