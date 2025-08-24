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
- `log_event` is used to track signups, logins, and activity.
- Database sessions are handled with `Depends(get_db)`.
"""

from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import SignupUser, ShowUser

from app.db.models import User
from app.services import log_event
from app.api.deps import TimedRoute, get_db, get_current_user
from app.services import auth
from app.services.user import crud_user
from app.core.enums import EventType, ObjectType


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)
router.route_class = TimedRoute


@router.post("/signup", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(payload: SignupUser, db: Session = Depends(get_db)) -> Any:
    """Register a new user (defaults to role=member). Logs the creation event."""
    created = auth.register(db, obj_in=payload)
    return created


@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """Authenticate user via OAuth2 form and return JWT. Logs login event."""
    logged = auth.login(form_data,db)
    user = db.query(User).filter(User.email == form_data.username).first()
    log_event(db, EventType.USER_LOGGED_IN, object_type=ObjectType.USER, user=user, status_code=201, method="POST",)
    return logged


