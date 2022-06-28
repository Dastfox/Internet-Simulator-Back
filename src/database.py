from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# creating sqlite

SQLALCHEMY_DATABASE_URL = "sqlite:///./hero.db"

engine = create_engine(
# connect args only in SQLite
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#  instantiated DB not a db until first use
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()