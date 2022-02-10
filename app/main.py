from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schema, utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# db
get_db()

@app.get("/")
def read_root():
    return {"Habib Rahman api is runing"}


@app.get("/posts", response_model = List[schema.PostRespone])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schema.PostRespone)
def createpost(post: schema.Post, db: Session = Depends(get_db)):
    new_posts = models.Post(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@app.get("/posts/{id}", response_model = schema.PostRespone)
def get_single_posts(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return (Response(status_code = status.HTTP_204_NO_CONTENT), delete_post)


@app.put("/posts/{id}", response_model = schema.PostRespone)
def update_post(id: int, post: schema.UpdatePost, db: Session = Depends(get_db)):
    my_post = db.query(models.Post).filter(models.Post.id == id)
    post_db = my_post.first()
    if post_db == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    my_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return my_post.first()


@app.post("/users", status_code = status.HTTP_201_CREATED, response_model = schema.UserResponse)
def createpost(user: schema.UserCreate, response: Response, db: Session = Depends(get_db)):
    # if user.email:
    #     userValid = db.query(models.User).filter(models.User.email == user.email).first()
    #     return {"msg": "User is Already Exist"}
        
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model = schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

    return user