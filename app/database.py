from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = "postgresql://postgres:p4stgr2s@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try: yield db
    except: db.close()