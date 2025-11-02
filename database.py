from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///listaapp.db")

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()