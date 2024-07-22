from sqlalchemy.orm import Session
import uuid
import random
import datetime

from core.models import tables


def get_user_history_by_id(user_id: uuid.UUID, db: Session):
    return db.query(tables.SoloSuggestionsHistory).filter(tables.SoloSuggestionsHistory.user_id==user_id).all()


def create_solo_suggestions_history(
    db: Session, user_id: uuid.UUID, query_dict, top_movies_imdb_ids: list[str]
):
    for imdb_id in top_movies_imdb_ids:
        existing_history = db.query(tables.SoloSuggestionsHistory).filter(
            tables.SoloSuggestionsHistory.user_id == user_id,
            tables.SoloSuggestionsHistory.movie_imdb_id == imdb_id
        ).first()
        
        if existing_history is None:
            movie = db.query(tables.Movie).filter(tables.Movie.imdb_id == imdb_id).first()
            new_history = tables.SoloSuggestionsHistory(
                user_id=user_id,
                query_dict=query_dict,
                movie_imdb_id=imdb_id,
                created_at=datetime.datetime.utcnow(),
                description=movie.description,
                title=movie.title 
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


def change_session_status(session_code: int, status: bool, db: Session):
    session = get_session_by_code(session_code, db)
    session.status = status
    db.add(session)
    db.commit()


def read_feedbacks(db: Session, imdb_id: str, user_id: uuid.UUID):
    feedback = (
        db.query(tables.Feedback)
        .filter(
            tables.Feedback.movie_imdb_id == imdb_id, tables.Feedback.user_id == user_id
        )
        .first()
    )
    return feedback


def update_movie_rating(rate: int, imdb_id: str, user_id: uuid.UUID, db: Session):
    feedback = read_feedbacks(db, imdb_id, user_id)
    if feedback:
        feedback.rate = rate
        db.add(feedback)
        db.commit()
    else:
        new_feedback = tables.Feedback(
            user_id=user_id, movie_imdb_id=imdb_id, rate=rate
        )
        db.add(new_feedback)
        db.commit()
    return {"status": "rating added"}


def update_movie_rating_in_history(user_id: uuid.UUID, movie_imdb_id: str, rating: int, db: Session):
    history_entry = db.query(tables.SoloSuggestionsHistory).filter(
        tables.SoloSuggestionsHistory.user_id == user_id,
        tables.SoloSuggestionsHistory.movie_imdb_id == movie_imdb_id
    ).all()
    for entrey in history_entry:
        if entrey:
            entrey.rating = rating
    db.commit()
    return history_entry