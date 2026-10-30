import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10},
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


def test_database_connection():
    if engine is None:
        raise RuntimeError("DATABASE_URL environment variable is not set.")

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar_one()