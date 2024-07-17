import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

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
