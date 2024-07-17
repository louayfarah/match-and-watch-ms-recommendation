import random
from core.models import tables
from sqlalchemy.orm import Session
import uuid


def create_session(user_id:uuid.UUID , db:Session):
    code = random.randint(100000, 999999)
    # code=uuid.uuid4()
    new_session = tables.Session(user_id=user_id, session_code=code)
    db.add(new_session)
    db.commit()
    return {"code":code}


def join_session(session_code: uuid.UUID, user_id: uuid.UUID, db: Session):
    session = db.query(tables.Session).filter(tables.Session.session_code == session_code).first()
    if not session:
            return {"error": "Session not found"}
    
    participant = db.query(tables.SessionParticipant).filter(tables.SessionParticipant.session_id==session.id, tables.SessionParticipant.user_id==user_id).first()
    if participant:
        return {"error": "You are already a participant in this session"}
    
    new_participant = tables.SessionParticipant(session_id=session.id, user_id=user_id)
    db.add(new_participant)
    db.commit()
    return {"message": "You have successfully joined the session"}


