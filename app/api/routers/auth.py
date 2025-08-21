from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.core import config, security
from app.core.enums import *
from app.schemas import schemas
from app.db.models.models import User
import app.api.deps as deps
from app.services import auth


router = APIRouter()

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)


@router.post("/signup", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.CreateUser, db: Session = Depends(deps.get_db)) -> Any:
    """
    Create new user without the need to be logged in.
    """
    return auth.register(db, obj_in=payload)


@router.post("/login")
def login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    return auth.login(form_data,db)


@router.get("/me", response_model=schemas.UserBase)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """
    user = current_user
    return user


