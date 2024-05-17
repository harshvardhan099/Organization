from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
  SQLALCHEMY_DATABASE_URL = "sqlite:///./Organization.db"
  
  engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
  )
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  
  Base = declarative_base()
  
  @staticmethod
  def get_db():
    db = Database.SessionLocal()
    try:
      yield db
    finally:
      db.close()
