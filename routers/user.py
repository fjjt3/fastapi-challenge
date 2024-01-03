from models import models, schemas
from sqlalchemy.orm import Session
from fastapi.params import Depends
from database import get_db
from routers.login import get_current_user
from fastapi import APIRouter, Query, HTTPException, status
from passlib.context import CryptContext


router = APIRouter(tags=['Users'],
                prefix="/user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/', response_model=schemas.DisplayUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_user = models.User(username=request.username, password=hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user