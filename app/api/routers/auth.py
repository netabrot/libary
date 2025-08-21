from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import (
    CreateUser, ShowUser,
)

from app.db.models import User
from app.services import log_event
from app.api.deps import get_db, get_current_user


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post("/signup", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(payload: CreateUser, db: Session = Depends(get_db)) -> Any:
    """
    Create new user without the need to be logged in.
    """
    data = payload.model_dump() 
    data.setdefault("role", "member")
    created = user.create(db, obj_in=payload)
    log_event(db, "user.created", created)
    return created


@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    logged = auth.login(form_data,db)
    log_event(db, "user.logged", logged)
    return logged


@router.get("/me", response_model=ShowUser)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Fetch the current logged in user.
    """
    user = current_user
    return user


