from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib
from .config import settings

# to escape any special char.
DB_PWD = urllib.parse.quote_plus(settings.DB_PWD)
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER_NAME}:{DB_PWD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
