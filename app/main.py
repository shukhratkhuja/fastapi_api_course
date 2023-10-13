from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# from requests import Response

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
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

@app.get("/posts")
def get_posts():
    
    cursor.execute("""SELECT * FROM public.posts""")
    posts = cursor.fetchall()
    
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    cursor.execute("""
                INSERT INTO public.posts(title, content, published)
                    VALUES(%s, %s, %s) 
                    RETURNING *
                """, (post.title, post.content, post.published))
    conn.commit()
    new_post = cursor.fetchone()
    
    return {"success": True, "data": new_post}

@app.get("/posts/latest")
def get_latest_post():
    
    return {"post_detail": my_posts[-1]}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    
    cursor.execute("SELECT * FROM public.posts WHERE id=%s", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post (id: int):
    
    cursor.execute("DELETE FROM public.posts WHERE id=%s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")


@app.put("/posts/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update_post (id: int, post: Post):

    cursor.execute("""
                    UPDATE public.posts SET title=%s, content=%s, published=%s WHERE id=%s
                   RETURNING*""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post:
        return {"success": True, "data": updated_post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")
