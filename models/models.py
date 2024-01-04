from sqlalchemy import Column, String
from database import Base


class Movie(Base):
    __tablename__ = 'movies'
    imdbID = Column(String, primary_key=True, index=True)
    title = Column(String)
    year = Column(String)
    poster = Column(String)
