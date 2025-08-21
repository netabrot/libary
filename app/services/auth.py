from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.models import User
from app.schemas.schemas import CreateUser
from app.core.security import *

from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

def login(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(
        User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

def register(db, *, obj_in: CreateUser) -> User:
        data = obj_in.model_dump(exclude={"password"})      
        plain = obj_in.password.get_secret_value()
        hashed = get_password_hash(plain)
        db_obj = User(**data, password=hashed)
        db.add(db_obj); db.commit(); db.refresh(db_obj)
        return db_obj