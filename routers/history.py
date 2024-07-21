from sqlalchemy.orm import Session
from core.schemas import schemas
from core.crud import crud
from dependencies import get_db, validate_user_token
from fastapi import APIRouter, Depends, HTTPException, status
from config import Config

conf = Config()
history_router = APIRouter()

@history_router.get("/api/history", status_code=200)
def get_user_history(
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(validate_user_token)
):
    user_id = user.get('id')
    history = crud.get_user_history_by_id(user_id, db)
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User history not found")
    return history






