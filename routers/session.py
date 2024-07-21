import requests
import uuid
from sqlalchemy.orm import Session
from core.schemas import schemas
from core.crud import crud
from dependencies import get_db, validate_user_token
from core.models import tables
from fastapi import APIRouter, Depends, HTTPException, status

from util import session_management
from load import df
from config import Config

conf = Config()
session_router = APIRouter(tags=["Multiple Users"])


@session_router.post("/api/submit-session-answer", status_code=201)
def submit_session_answer(
    session_code: int,
    answers: str,
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
):
    session = crud.get_session_by_code(session_code, db)
    if not session:
        raise HTTPException(
            status_code=404, detail="Session not found or already closed"
        )
    user_submitted = crud.get_user_by_session_id(user.get("id"), session.id, db)
    if user_submitted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submited your answers ",
        )
    new_answer = tables.Answer(
        session_id=session.id, user_id=user.get("id"), answers=answers
    )
    db.add(new_answer)
    db.commit()
    return {"status": "answers submitted"}


@session_router.get("/api/generate-session-code")
def generate_code(
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
    db: Session = Depends(get_db),
):
    return session_management.create_session(user.get("id"), db)


@session_router.post("/api/join-session/{session_code}", status_code=201)
def join_session(
    session_code: int,
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
):
    return session_management.join_session(session_code, user.get("id"), db)


@session_router.post(
    "/api/close-session", status_code=201, response_model=list[schemas.Movie]
)
def close_session(
    session_code: int,
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
):
    return session_management.close_session(session_code, user.get("id"), db)
