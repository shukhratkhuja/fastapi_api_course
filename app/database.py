from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
import psycopg2, time
from psycopg2.extras import RealDictCursor


# SQLALCHEMY_DB_URL = "postgresql://shukhratkhuja:p4stgr2s@localhost/analytic_backup"
SQLALCHEMY_DB_URL="postgresql://shukhratkhuja:%s@127.0.0.1/analytic_backup" % quote('p4stgr2s') #, echo=True

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()

    try: 
        yield db
    except: 
        db.close()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='analytic_backup', 
            user='shukhratkhuja', 
            password='p4stgr2s', 
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("ERROR: ", str(error))
        time.sleep(5)
