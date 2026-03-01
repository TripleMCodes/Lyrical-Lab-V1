from sqlalchemy import select
from datetime import datetime, timedelta
from sqlalchemy import func, text
from .. import models, schemas, utils
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base, Users, Lyrics
from app.schemas import UserCreate, UserOut
from app import oauth2, models, database

router = APIRouter(
    prefix="/api/users",
    tags=['users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    #hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/stats", status_code=status.HTTP_200_OK)
def get_stats(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    stats = (
        db.query(models.Stats)
        .filter(models.Stats.user_id == int(current_user.uid))
        .first()
    )

    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stats not found for user",
        )

    return stats

@router.get("/song-quantity")
def get_song_num(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    one_week_ago = datetime.now() - timedelta(days=7)

    total_songs = (
        db.query(func.count(models.Lyrics.song_id))
        .filter(models.Lyrics.user_id == current_user.uid)
        .scalar()
    )

    new_songs = (
        db.query(func.count(models.Lyrics.song_id))
        .filter(
            models.Lyrics.user_id == current_user.uid,
            models.Lyrics.date_created >= one_week_ago,
        )
        .scalar()
    )

    return {
        "num_songs": total_songs,
        "new_songs": new_songs,
    }


@router.get("/draft", status_code=status.HTTP_200_OK)
def get_draft(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    draft = (
        db.query(models.StateFold)
        .filter(models.StateFold.user_id == current_user.uid)
        .first()
    )

    if draft is None:
        return {
            "id": None,
            "song_name": "",
            "song_genre": "",
            "song_lyrics": "",
            "song_artist": "",
            "song_mood": "",
            "song_album": "",
        }

    return draft

@router.get('/recent-songs', status_code=status.HTTP_200_OK)
def get_recent_songs(
    db:Session = Depends(get_db),
    current_user: models.Users = Depends(oauth2.get_current_user)
):
    
    recent_songs = (
    db.query(models.Lyrics)
    .filter(
        models.Lyrics.user_id == current_user.uid,
        models.Lyrics.date_created >= func.now() - text("interval '7 days'")
    )
    .all()
    )
   
    if recent_songs is None:
        return []

    return recent_songs


@router.get("/{id}", response_model=UserOut)
def get_user(id:int, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found")
    
    return user



@router.get("/dashboard/writing-stats")
def dashboard_writing_stats(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(oauth2.get_current_user),
):

    stmt = (
        select(
            models.Stats.date_created,
            models.Stats.total_writing_time,
            models.Stats.writing_sessions,
        )
        .where(models.Stats.user_id == current_user.uid)
        .order_by(models.Stats.date_created.asc())
    )
    
    rows = db.execute(stmt).all()

    return [
        {
            "date": r.date_created.date() if r.date_created.date() else None,
            "writing_time": int(r.total_writing_time or 0),
            "sessions": int(r.writing_sessions or 0),
        }
        for r in rows
    ]