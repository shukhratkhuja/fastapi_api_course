from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
import psycopg2, time
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DB_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" #echo=True
print(SQLALCHEMY_DB_URL)

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()

    try: 
        yield db
    except: 
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host=settings.database_hostname, 
#             database=settings.database_name, 
#             user=settings.database_username, 
#             password=settings.database_password, 
#             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("ERROR: ", str(error))
#         time.sleep(5)
