from models import models, schemas
from models.schemas import User
from routers.login import get_current_user
from sqlalchemy.orm import Session
from fastapi.params import Depends
from database import get_db
from typing import List
from fastapi import APIRouter, Query, HTTPException

router =  APIRouter(tags=['Movies'],
                    prefix="/movie")



@router.get('/', response_model=List[schemas.Movie]) 
def get_movies(db: Session = Depends(get_db), 
            limit: int = Query(10, description="Número de películas por página"), 
            offset: int = Query(5, description="Número de películas a omitir")):
    movies = db.query(models.Movie).order_by(models.Movie.title).offset(offset).limit(limit).all() 
    return movies

@router.get('/{title}', response_model=schemas.Movie)
def get_movie_by_title(title: str, db: Session = Depends(get_db), 
                    current_user: schemas.User = Depends(get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.title == title).first()
    return movie

@router.post('/', response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete('/{imdbID}')
def delete_movie(imdbID: str, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.imdbID == imdbID).first()
    if movie:
        db.delete(movie)
        db.commit()
        return {"message": "Movie deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Movie not found")