from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config

conf = Config()

engine = create_engine(conf.get_database_connection_string())
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
