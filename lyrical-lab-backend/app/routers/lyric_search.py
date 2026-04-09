from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

import models
import database
import oauth2
from app import schemas, oauth2, models, database
from app.services import search_user_lyrics 

router = APIRouter(
    prefix="/lyrics-search",
    tags=["Lyrics Search"],
)


@router.get("/", status_code=status.HTTP_200_OK)
def search_lyrics(
    q: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20),
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):

    results = search_user_lyrics(
        query=q,
        user_id=current_user.uid,
        db=db,
        top_k=top_k,
    )

    return {
        "query": q,
        "results": results,
        "count": len(results),
    }