from sqlalchemy import Column, Integer, String
from database import Base


class Movie(Base):
    __tablename__ = 'movies'
    imdbID = Column(String, primary_key=True, index=True)
    title = Column(String)
    year = Column(String)
    poster = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    