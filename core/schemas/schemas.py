import uuid

from typing import List
from pydantic import BaseModel







class AuthenticatedUser(BaseModel):
    email: str | None = None
    id: uuid.UUID
    name: str | None = None
    surname: str | None = None
    has_logged_in: bool
