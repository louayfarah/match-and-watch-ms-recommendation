import uuid
from pydantic import BaseModel, ConfigDict


class AuthenticatedUser(BaseModel):
    email: str | None = None
    id: uuid.UUID
    name: str | None = None
    surname: str | None = None
    has_logged_in: bool


class Movie(BaseModel):
    id: uuid.UUID
    imdb_id: str
    title: str
    type: str
    description: str
    release_year: int
    age_certification: str
    runtime: int
    genres: str
    imdb_score: float
    emotions: str
    length: str
    platform: str
    model_config = ConfigDict(from_attributes=True)
