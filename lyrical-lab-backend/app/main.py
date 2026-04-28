from datetime import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.params import Body

from app.database import engine, get_db
from app.models import Base, Users, ContactMessages
from .routers import auth, user
from .routers.lyrical_tools import lyrical_lab
from .routers import lyric_search
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
    return {"message": "Hello world!"}

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
