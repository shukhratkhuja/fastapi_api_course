from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .utils import hash
from .routers import post, user

# from requests import Response

models.Base.metadata.create_all(bind=engine) 

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='p4stgr2s', 
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("ERROR: ", str(error))
        time.sleep(5)


app.include_router(post.router)
app.include_router(user.router)


@app.get("/") 
def root():
    return {'message': 'Hello from FastAPI!'}

















# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=56678s 6.11
