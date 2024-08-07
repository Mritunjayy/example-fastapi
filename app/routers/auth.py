from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
router= APIRouter(tags= ["Authentication"])

@router.post("/login", response_model=schemas.Token)
# def login(#user_credentials: schemas.UserLogin
def login(user_credentials: OAuth2PasswordRequestForm = Depends( ), db: Session = Depends(get_db)):

    ##user_crendentials= OAuth2PasswordRequestForm will generate not email and password rather username and password , like
    # {
    #     "username": "aadaayd",
    #     "password": "daevy"
    # }
    ##therefore we change the below query from user_credentials.email to-> user_credentials.username
    # print(db)
    # print(user_credentials)
    user= db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=  status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!!!!!!!!!")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    #cretae token
    #return token

    access_token= oauth2.create_access_token(data= {"user_id": user.id} )
    return {"access_token":access_token, "token_type":"bearer"}


    