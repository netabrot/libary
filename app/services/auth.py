from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.enums import UserRole
from app.db.models.user import User
from app.core.security import *

from sqlalchemy.orm import Session

from app.schemas.users import SignupUser

def login(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(
        User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

def register(db, *, obj_in: SignupUser) -> User:
    existing_user = db.query(User).filter(User.email == obj_in.email.lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = obj_in.model_dump(exclude={"password"})
    plain_password = obj_in.password.get_secret_value()
    password = get_password_hash(plain_password)

    new_user = User(
        full_name=user_data["full_name"],
        email=user_data["email"], 
        phone_number=user_data["phone_number"],
        address=user_data.get("address"),
        password=password,
        role=UserRole.MEMBER,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user