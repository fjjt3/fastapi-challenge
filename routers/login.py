from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models import models, schemas
from database import get_db
from models.schemas import TokenData
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2AuthorizationCodeBearer


SECRET_KEY = "******"
ALGORITHM = "*****"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=['Login'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect username or password')
    # Verify the hashed password with the entered one
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
    # Gen JWT token
    access_token = generate_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type":"bearer"}

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception