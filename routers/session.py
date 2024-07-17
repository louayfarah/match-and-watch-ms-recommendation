import requests
import uuid
from sqlalchemy.orm import Session
from core.schemas import schemas
from core.crud import crud
from dependencies import get_db, validate_user_token
from core.models import tables
from fastapi import APIRouter, Depends, HTTPException,status

from util import session_management
from load import df
from config import Config

conf = Config()
session_router = APIRouter(tags=["Session"])



@session_router.get("/generate/session/code")
def generate_code(
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
    db: Session = Depends(get_db),
):
    return session_management.create_session(user.get('id'),db)

@session_router.post("/join_session/{session_code}")
def join_session(
    session_code: uuid.UUID,
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
):
    return session_management.join_session(session_code,user.get('id'),db)


# @session_router.get("/for testing")
# def delete():
#     response = requests.post(
#         "http://backend:8000/check/user/token",
#         json={"token": "token"}
#     )
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#         )


