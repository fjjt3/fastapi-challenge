from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
    title: str
    year: str
    imdbID: str
    poster: str

class MovieCreate(BaseModel):
    title: str
    year: str
    imdbID: str
    poster: str

class User(BaseModel):
    username: str
    password: str

class DisplayUser(BaseModel):
    username: str

    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional [str] = None    