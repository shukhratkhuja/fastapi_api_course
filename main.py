from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
# from requests import Response

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
app = FastAPI()


my_posts = [{"title":"First Post", "content":"First Post Content", "id": 1}, {"title":"Fresh Fruits", "content":"Some usefull information about fresh fruits", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/") 
def root():
    return {'message': 'Hello from FastAPI!'}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000000)

    my_posts.append(post_dict)
    
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    return {"post_detail": my_posts[-1]}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post (id: int):
    index = find_post_index(id)
    if index is not None:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")


@app.put("/posts/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update_post (id: int, post: Post):
    
    index = find_post_index(id)
    post_dict = post.dict()
    if index is not None:

        post_dict['id'] = id
        my_posts[index] = post_dict
        return post_dict
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")