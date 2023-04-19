import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.config import settings
from apps.main import app
from apps.database import get_db

# Escape any special char, if any.
DB_PWD = urllib.parse.quote_plus(settings.DB_PWD)
# Test DB Name will have "-test" suffix.
SQLALCHEMY_TEST_DATABASE_URL = f"postgresql://{settings.DB_USER_NAME}:{DB_PWD}@{settings.DB_HOST}/{settings.DB_NAME}-test"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_test_db():
    db = TestSessionLocal()
    """In Python, the __call__ method is invoked on an object when it is "called" in the same way as a function:
    Session = sessionmaker()
    session = Session()  # invokes sessionmaker.__call__()
    """
    try:
        yield db
    finally:
        db.close()


# Set dependency override, so that code replace reference to "get_db" dependency with "test_get_db" during test run.
app.dependency_overrides[get_db] = get_test_db
