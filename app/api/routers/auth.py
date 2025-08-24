"""
Authentication Router
---------------------

This file defines the API endpoints for user authentication and self-service.

Endpoints:
- POST /auth/signup → Create a new user (no login required, defaults to 'member' role)
- POST /auth/login  → Authenticate a user and return a JWT token
- GET /auth/me      → Fetch the currently logged-in user's details

Notes:
- JWT-based authentication using OAuth2PasswordRequestForm for login.
- Database sessions are handled with `Depends(get_db)`.
"""

from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import SignupUser, ShowUser

from app.db.models import User
from app.api.deps import get_current_user
from app.services import auth
from app.db import get_db


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post("/signup", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(payload: SignupUser, db: Session = Depends(get_db)) -> Any:
    """Register a new user (defaults to role=member). Logs the creation event."""
    created = auth.register(db, obj_in=payload)
    return created


@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """Authenticate user via OAuth2 form and return JWT. Logs login event."""
    logged = auth.login(form_data, db)
    return logged


@router.get("/me", response_model=ShowUser)
def get_current_user_info(current_user: User = Depends(get_current_user)) -> Any:
    """Get the currently logged-in user's details."""
    return current_user


