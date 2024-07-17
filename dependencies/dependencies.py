import core
import core.databases
import core.databases.postgres
import core.databases.postgres.postgres
import core.schemas
import core.schemas.schemas


def get_db():
    db = core.databases.postgres.postgres.session_local()
    try:
        yield db
    finally:
        db.close()
