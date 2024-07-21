from sqlalchemy.orm import Session
import uuid
from core.models import tables
from core.crud import crud
from fastapi import HTTPException, status

def add_rating(rate: int, movie_imdb_id: str, user_id: uuid.UUID, db: Session):
    movie = crud.get_movie_by_imdb_id(movie_imdb_id, db)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    crud.create_feedback(
        movie_imdb_id=movie_imdb_id, user_id=user_id, rate=rate, db=db
    )
    return {"feedback added successfully"}

