from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote


models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/") 
def root():
    return {'message': 'Hello from FastAPI!'}

















# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=56678s 6.11
