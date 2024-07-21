import requests
from fastapi import HTTPException,status

import core.databases.postgres.postgres

from config import Config
conf = Config()


def get_db():
    db = core.databases.postgres.postgres.session_local()
    try:
        yield db
    finally:
        db.close()

def validate_user_token(token: str):
    response = requests.post(
        f"{conf.get_user_microservice_url()}",
        json=token
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
