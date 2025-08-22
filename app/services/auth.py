from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.user import User
from app.core.security import *

from sqlalchemy.orm import Session

def login(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(
        User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Credentials")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect password")

    access_token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


#TODO: Register