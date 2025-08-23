from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.user import User
from app.core.security import *

from sqlalchemy.orm import Session

from app.schemas.users import CreateUser

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

def register(db, *, obj_in: CreateUser) -> User:
            data = obj_in.model_dump(exclude={"password","role", "is_active"})      
            plain = obj_in.password.get_secret_value()
            hashed = get_password_hash(plain)
            db_obj = User(**data, password=hashed, role="member", is_active=True)
            db.add(db_obj); db.commit(); db.refresh(db_obj)
            return db_obj
