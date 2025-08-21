from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.core import config, security
from app.core.enums import *
from app.schemas.schemas import EventBase, ShowUser, CreateUser
from app.db.models.models import User
import app.api.deps as deps
from app.services import auth
from app.services.user import crud_user as user
from app.services.event import log_event


router = APIRouter()

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post("/signup", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(payload: CreateUser, db: Session = Depends(deps.get_db)) -> Any:
    """
    Create new user without the need to be logged in.
    """
    data = payload.model_dump() 
    data.setdefault("role", "member")
    created = user.create(db, obj_in=payload)
    log_event(db, "user.created", created)
    return created


@router.post("/login")
def login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    logged = auth.login(form_data,db)
    log_event(db, "user.logged", logged)
    return logged


@router.get("/me", response_model=ShowUser)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """
    user = current_user
    return user


