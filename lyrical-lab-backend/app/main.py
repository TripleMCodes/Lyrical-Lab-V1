from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
# from scipy import stats
from sqlalchemy.orm import Session
from fastapi.params import Body

from app.database import engine, get_db
from app.models import Base, Users, ContactMessages
from .routers import auth, user
from .routers.lyrical_tools import lyrical_lab
from .routers import lyric_search
from app.routers.lyrical_tools.lyrical_lab import find_rhymes
from datetime import datetime, timedelta
from app import schemas, oauth2, models, database
# from app.services import initialize_embeddings
# from app.lyrics_n_summarization import OpenRouterClient

app = FastAPI()
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


# @app.on_event("startup")
# def on_startup():
#     """Initialize embeddings and other resources on app startup."""
#     initialize_embeddings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router) 
app.include_router(lyrical_lab.router)
# app.include_router(lyric_search.router)


@app.get("/")
async def index():
    return {"message": "Hello world! This is M-Prosody"}

@app.post("/api/contact")
async def get_users(msg:dict, db: Session = Depends(get_db)):
    print(f"this is the message")
    email = msg["email"]
    subject = msg["subject"]
    message = msg["message"]
    date_created = datetime.utcnow()

    db_message = ContactMessages(email=email, subject=subject, message=message, date_created=date_created)
    db.add(db_message)
    db.commit()

    return {"message": "Message received!"}

#TODO: ADD API KEY BASED RATE LIMITING
@app.post("/api/public/get-rhymes")
async def find_rhymes_public(
    data: dict, 
    public: int = 2,
    db: Session = Depends(database.get_db)
):
    MAX_REQUESTS_PER_DAY = 10 # FOR TESTING

    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    # Get today's request count
    today_limit = db.query(models.APIRequestLimit).filter(
        models.APIRequestLimit.user_id == public,
        models.APIRequestLimit.date_created >= start_of_day,
        models.APIRequestLimit.date_created < end_of_day,
    ).first()

    if today_limit and today_limit.request_count >= MAX_REQUESTS_PER_DAY:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"You have reached your daily limit of {MAX_REQUESTS_PER_DAY} requests. Please try again tomorrow."
        )
    
    # Increment request count
    if today_limit:
        today_limit.request_count += 1
    else:
        today_limit = models.APIRequestLimit(
            user_id=public,
            request_count=1,
            date_created=now
        )
        db.add(today_limit)
    
    db.commit()
    res = find_rhymes(data)
    return res