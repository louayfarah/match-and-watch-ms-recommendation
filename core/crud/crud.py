from sqlalchemy.orm import Session
import uuid
import random

from core.models import tables


def create_session(user_id: uuid.UUID, db: Session):
    code = random.randint(100000, 999999)
    new_session = tables.Session(user_id=user_id, session_code=code)
    db.add(new_session)
    db.commit()
    return {"code": code, "session_id": new_session.id, "status": new_session.status}


def get_session_by_code(session_code: int, db: Session):
    return (
        db.query(tables.Session)
        .filter(tables.Session.session_code == session_code)
        .first()
    )


def get_participant_by_session_id(session_id: int, user_id: uuid.UUID, db: Session):
    return (
        db.query(tables.SessionParticipant)
        .filter(
            tables.SessionParticipant.session_id == session_id,
            tables.SessionParticipant.user_id == user_id,
        )
        .first()
    )


def add_participant(session_id: int, user_id: uuid.UUID, db: Session):
    new_participant = tables.SessionParticipant(session_id=session_id, user_id=user_id)
    db.add(new_participant)
    db.commit()


def close_session_by_code(session_code: int, db: Session):
    session = get_session_by_code(session_code, db)
    if session:
        session.status = False
        db.commit()
    return session
