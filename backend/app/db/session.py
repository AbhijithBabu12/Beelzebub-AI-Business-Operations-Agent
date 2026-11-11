from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


# Create database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db():
    """
    Provides a database session for each request.

    Ensures that the session is closed after use.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()