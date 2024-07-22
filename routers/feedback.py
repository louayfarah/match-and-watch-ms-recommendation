from fastapi import APIRouter, Depends, HTTPException, status
from core.schemas import schemas
from sqlalchemy.orm import Session
from dependencies import get_db, validate_user_token
from core.crud import crud

feedback_router = APIRouter(tags=["Feedback"])


@feedback_router.post("/api/rate/movie", status_code=201)
def update_rating(
    rate: int,
    movie_imdb_id: str,
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
    db: Session = Depends(get_db),
):
    try:
        crud.update_movie_rating(rate, movie_imdb_id, user.get("id"), db)
        return {"status": "rating added"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
