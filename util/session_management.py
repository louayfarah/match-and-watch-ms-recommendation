import torch
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.crud import crud
import uuid
from core.models import tables
from util import find_top_movies, extend_top_movies
from load import df


def create_session(user_id: uuid.UUID, db: Session):
    return crud.create_session(user_id, db)


def join_session(session_code: int, user_id: uuid.UUID, db: Session):
    session = crud.get_session_by_code(session_code, db)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    if not session.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is closed and cannot be joined",
        )

    participant = crud.get_participant_by_session_id(session.id, user_id, db)
    if participant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a participant in this session",
        )

    crud.add_participant(session.id, user_id, db)
    return {"message": "You have successfully joined the session"}


def close_session(session_code: int, user_id: uuid.UUID, db: Session):
    session = crud.get_session_by_code(session_code, db)
    is_creater = crud.get_session_creater(user_id, session.id, db)
    if not is_creater:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only the creator can close the session",
        )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    if not session.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Session is already closed"
        )

    answers_tuples = (
        db.query(tables.Answer.answers)
        .filter(tables.Answer.session_id == session.id)
        .all()
    )
    all_answers = [answers[0] for answers in answers_tuples]

    if len(all_answers) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No answers submitted for this session",
        )

    recommended_movies = find_top_movies(
        df, all_answers, number_of_users=len(all_answers)
    )
    res = extend_top_movies(db, recommended_movies)
    crud.change_session_status(session_code, False, db)
    return res
