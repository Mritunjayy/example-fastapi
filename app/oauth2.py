"""Choose python-jose[cryptography] for a broader range of cryptographic operations and standards, and pyjwt for straightforward JWT handling."""

from jose  import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme= OAuth2PasswordBearer(tokenUrl= "login")

#SECRET_KEY  (this also needs to be hided or something must be done)-->so we use environment variables..
#Algorithm
#Expiration time(total time a user can be logged in , afetr this expires, user need to log in again)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire= datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiration": expire})
    for key, value in to_encode.items():
        if isinstance(value, datetime):
            to_encode[key] = value.isoformat()

    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id :str= payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id= id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    # return verify_access_token(token, credentials_exception)

