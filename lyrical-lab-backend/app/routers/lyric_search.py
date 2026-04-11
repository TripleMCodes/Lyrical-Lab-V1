from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from app import schemas, oauth2, models, database
from app.services import search_user_lyrics 

router = APIRouter(
    prefix="/lyrics-search",
    tags=["Lyrics Search"],
)


@router.get("/", status_code=status.HTTP_200_OK)
def search_lyrics(
    q: str = Query(..., min_length=1, max_length=500),
    top_k: int = Query(5, ge=1, le=20),
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    """
    Search user's lyrics with a query string.
    
    Query Parameters:
    - q: Search query (required, 1-500 characters)
    - top_k: Number of results to return (1-20, default 5)
    
    Returns:
    - query: The search query used
    - results: List of matching lyrics with scores and snippets
    - count: Number of results returned
    """
    
    try:
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
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(ve)}"
        )
    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search service error: {str(re)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during search: {str(e)}"
        )