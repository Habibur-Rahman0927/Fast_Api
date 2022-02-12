from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Post):
    pass

class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode=True

class PostRespone(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode=True

class Postout(BaseModel):
    Post: PostRespone
    votes: int

    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)