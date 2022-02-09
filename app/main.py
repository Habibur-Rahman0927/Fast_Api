from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg2.connect(host="localhost", database='FastApi', user="postgres", password='asdf1234', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesfull")
except Exception as error:
    print("connect to database failed")
    print("Error", error)


my_posts = [
    {"id": 1, "title": "title of post 1", "content": "content of post 1"},
    {"id": 2, "title": "title of post 2", "content": "content of post 2"},
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"Habib Rahman api is runing"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def createpost(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *", (post.title, post.content, post.published))
    posts = cursor.fetchone()
    conn.commit()
    return {"data": posts}


@app.get("/posts/{id}")
def get_single_posts(id: int, response: Response):
    cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return (Response(status_code = status.HTTP_204_NO_CONTENT), {"delete_data": delete_post})


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ", (post.title, post.content, post.published, str(id)))
    my_posts = cursor.fetchone()
    conn.commit()
    if my_posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"data": my_posts}

