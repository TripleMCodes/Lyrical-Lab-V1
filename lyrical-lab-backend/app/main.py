from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.params import Body

from app.database import engine, get_db
from app.models import Base, Users
from .routers import auth, user
from .routers.lyrical_tools import lyrical_lab
# from app.lyrics_n_summarization import OpenRouterClient

app = FastAPI()
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)


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

@app.get("/")
async def index():
    return {"Message": "Hello world!"}

@app.get("/api/test")
async def get_users(db: Session = Depends(get_db)):
    return db.query(Users).all()


