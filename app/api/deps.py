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
from typing import Generator
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware


from app.db.session import SessionLocal
from app.db.models import User    
from app.db import get_db    
from app.core.security import verify_token
from app.core.enums import UserRole
from app.services.event import log_event
from app.utils import filters


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """Validate JWT token and return the current active user."""
    token_data = verify_token(token) 
    user = db.query(User).filter(User.id == int(token_data.sub)).first()
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

def require_roles(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)):
        """Ensure the current user has one of the allowed roles."""
        if current_user.role not in allowed_roles:
            roles_str = " or ".join([role.value for role in allowed_roles])
            raise HTTPException(
                status_code=403,
                detail=f"{roles_str} only"
            )
        return current_user
    return role_checker

class ResponseTimeMiddleware(BaseHTTPMiddleware):
    SKIP_PATHS = {"/", "/test"}

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        start = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = int((time.perf_counter() - start) * 1000)
        response.headers["X-Response-Time"] = str(duration_ms)

        try:
            user_id: int | None = None
            auth = request.headers.get("authorization")
            if auth and auth.startswith("Bearer "):
                try:
                    data = verify_token(auth.split(" ", 1)[1])
                    if data and data.sub:
                        user_id = int(data.sub)
                except (JWTError, ValueError, TypeError):
                    pass

            meta = {
                "path": request.url.path,
                "method": request.method,
                "query_params": str(request.query_params) or None,
                "user_agent": request.headers.get("user-agent"),
                "content_length": response.headers.get("content-length"),
                "remote_addr": getattr(request.client, "host", None),
            }
            meta = filters(**meta)

            with SessionLocal() as db:
                log_event(
                    db=db,
                    user_id=user_id, 
                    status_code=response.status_code,
                    method=request.method,
                    duration_ms=duration_ms,
                    meta=meta,
                )
                db.commit()
        except Exception:
            pass

        return response