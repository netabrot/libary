"""
Dependencies
------------

Shared FastAPI dependencies for database sessions, authentication, 
and role-based authorization.

Functions:
- get_db()             → Provide a SQLAlchemy session (auto-closes after request).
- get_current_user()   → Extract and validate current user from JWT.
- require_role(role)   → Dependency factory to enforce a specific UserRole.
"""

import time
from typing import Callable, Generator
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.user import User  
from app.core.security import verify_token
from app.core.enums import EventType, UserRole
from app.services.event import log_event


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db() -> Generator:
    """Provide a database session (closes after request)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """Validate JWT token and return the current active user."""

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception) 
    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user

def require_role(required_role: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        """Ensure the current user has the required role."""
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"{required_role.value} only"
            )
        return current_user
    return role_checker

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            
            db = SessionLocal()
            try:
                user = getattr(request.state, "user", None)
                meta = {
                    "path": request.url.path,
                    "method": request.method,
                    "user_id": request.headers.get("user_id")}
                log_event(
                    db,
                    EventType.HTTP_COMPLETED,
                    user=user,
                    status_code=response.status_code,
                    method=request.method,
                    duration_ms=duration,
                    **meta,
                )
            except Exception:
                db.rollback()
            finally:
                db.close()

        return custom_route_handler