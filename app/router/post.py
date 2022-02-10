from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()






@router.get("/posts", response_model = List[schema.PostRespone])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schema.PostRespone)
def createpost(post: schema.Post, db: Session = Depends(get_db)):
    new_posts = models.Post(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/posts/{id}", response_model = schema.PostRespone)
def get_single_posts(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post


@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return (Response(status_code = status.HTTP_204_NO_CONTENT), delete_post)


@router.put("/posts/{id}", response_model = schema.PostRespone)
def update_post(id: int, post: schema.UpdatePost, db: Session = Depends(get_db)):
    my_post = db.query(models.Post).filter(models.Post.id == id)
    post_db = my_post.first()
    if post_db == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    my_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return my_post.first()
