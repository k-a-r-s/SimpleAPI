from pydantic import BaseModel
from datetime import datetime


class Create_user(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    created_at: datetime


class Post(BaseModel):
    title: str
    description: str
    owner_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Vote(BaseModel):
    post_id: int
    dir: int


class Votes_out(BaseModel):
    post_id: int
    user_id: int
    post_info: Post
    owner_info: User


class Vote_out(BaseModel):
    user_id: int
