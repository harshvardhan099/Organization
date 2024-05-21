from typing import Generator, Any
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel.orm.session import Session


class Database:
  SQLALCHEMY_DATABASE_URL = "sqlite:///./Organization.db"
  
  engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
  )
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  
  Base = declarative_base()
  
  @staticmethod
  def get_db() -> Generator[Session, Any, None]:
    db = Database.SessionLocal()
    try:
      yield db  # type: ignore
    finally:
      db.close()
