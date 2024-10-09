from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import models, schemas, oauth2, database

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get(path="", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db),
            current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10,
            offset: int = 0,
            search: Optional[str] = "" # type: ignore
            ):

    posts = db.query(models.Post).filter(
        or_(models.Post.title.ilike(f"%{search}%"),
            models.Post.content.ilike(f"%{search}%")
            )
        ).limit(limit).offset(offset).all() # .filter(models.Post.owner_id == current_user.id).all()
    
    return posts


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(database.get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
        
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) # post.dict() changed to post.model_dump becouse of method deprication
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, response: Response, db: Session = Depends(database.get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")
        
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT, response_model=schemas.Post)
def update_post(id: int, post: schemas.Post, db: Session = Depends(database.get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    db_post = post_query.first()
    
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists!")
       
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
