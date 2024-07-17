import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime,Integer,Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    imdb_id = Column(String(255))
    title = Column(String(255))
    type = Column(String(255))
    description = Column(String(100000))
    release_year = Column(Integer)
    age_certification = Column(String(255))
    runtime = Column(Integer)
    genres = Column(
        String(255),
    )
    imdb_score = Column(Float)
    emotions = Column(String(255))
    length = Column(String(255))
    platform = Column(String(255))

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False) 
    session_code = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    participants = relationship(
        "SessionParticipant", backref="session", cascade="all, delete-orphan"
    )

class SessionParticipant(Base):
    __tablename__ = 'session_participants'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.id'), index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False) 
    joined_at = Column(DateTime, default=datetime.utcnow)
