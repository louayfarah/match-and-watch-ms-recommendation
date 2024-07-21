from sqlalchemy.orm import Session
import uuid
import random
import datetime

from core.models import tables


def create_solo_suggestions_history(
    db: Session, user_id: uuid.UUID, query_string: str, top_movies_imdb_ids: list[str]
):
    new_history = tables.SoloSuggestionsHistory(
        user_id=user_id,
        query_string=query_string,
        suggestions=top_movies_imdb_ids,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(new_history)
    db.commit()


def create_session(user_id: uuid.UUID, db: Session):
    code = random.randint(100000, 999999)
    new_session = tables.Session(user_id=user_id, session_code=code)
    db.add(new_session)
    db.commit()
    add_participant(session_id=new_session.id, user_id=user_id, db=db)
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


def get_movie_by_imdb_id(imdb_id:str , db: Session):
    return db.query(tables.Movie).filter(tables.Movie.imdb_id==imdb_id).first()

def create_feedback(rate: int, movie_imdb_id: str, user_id: uuid.UUID, db: Session):
    new_feedback = tables.Feedback(
        movie_imdb_id=movie_imdb_id, user_id=user_id, rate=rate
    )
    db.add(new_feedback)
    db.commit()
    
def read_movie_details(db: Session, imdb_id: str) -> tables.Movie | None:
    ans = db.query(tables.Movie).filter(tables.Movie.imdb_id == imdb_id).first()
    print(ans)

    return ans


def get_user_by_session_id(user_id: uuid.UUID, session_id: int, db: Session):
    return (
        db.query(tables.Answer)
        .filter(
            tables.Answer.session_id == session_id, tables.Answer.user_id == user_id
        )
        .first()
    )


def get_session_creater(user_id: uuid.UUID, session_id: int, db: Session):
    return (
        db.query(tables.Session)
        .filter(tables.Session.user_id == user_id, tables.Session.id == session_id)
        .first()
    )

def change_session_status(session_code: int,status:bool, db: Session):
    session=get_session_by_code(session_code,db)
    session.status=status
    db.add(session)
    db.commit()
