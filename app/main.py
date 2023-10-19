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


@app.get("/") 
def root():
    return {'message': 'Hello from FastAPI!'}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM public.posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute("""
    #             INSERT INTO public.posts(title, content, published)
    #                 VALUES(%s, %s, %s) 
    #                 RETURNING *
    #             """, (post.title, post.content, post.published))
    # conn.commit()
    # new_post = cursor.fetchone()
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# @app.get("/posts/latest")
# def get_latest_post():
    
#     return {"post_detail": my_posts[-1]}

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id:int, response: Response, db: Session = Depends(get_db)):
    
    # cursor.execute("SELECT * FROM public.posts WHERE id=%s", (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post (id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("DELETE FROM public.posts WHERE id=%s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first():
        post.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")


@app.put("/posts/{id}", status_code=status.HTTP_205_RESET_CONTENT, response_model=schemas.Post)
def update_post (id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""
    #                 UPDATE public.posts SET title=%s, content=%s, published=%s WHERE id=%s
    #                RETURNING*""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    db_post = post_query.first()
    
    if db_post:
        post_query.update(post.dict(), synchronize_session=False)
        db.commit() 
        return post_query.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")

