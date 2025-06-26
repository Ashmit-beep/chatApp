# app/db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# point at a local SQLite file
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat.db"

# create the engine
# for SQLite, you need check_same_thread=False under ASGI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# create a Session class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# base class for your models
Base = declarative_base()
