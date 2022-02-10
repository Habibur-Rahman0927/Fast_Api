from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, jwt
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model = List[schema.PostRespone])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schema.PostRespone)
def createpost(post: schema.Post, db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    new_posts = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/{id}", response_model = schema.PostRespone)
def get_single_posts(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return (Response(status_code = status.HTTP_204_NO_CONTENT), delete_post)


@router.put("/{id}", response_model = schema.PostRespone)
def update_post(id: int, post: schema.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    my_post = db.query(models.Post).filter(models.Post.id == id)
    post_db = my_post.first()
    if post_db == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    my_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return my_post.first()
