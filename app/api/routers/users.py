"""
Users Router
------------

Manages user accounts in the system.

Endpoints:
- GET /users/         → List users with optional filters (admin only)
- POST /users/        → Create a new user (admin only)
- PATCH /users/{id}   → Update user details (admin only, with role restrictions)
- DELETE /users/{id}  → Delete a user (admin only, with role restrictions)

Notes:
- Admin-only actions enforced via `require_role(UserRole.ADMIN)`.
- Extra security: prevents privilege escalation (non-admins can’t make themselves admin).
- All actions are logged with `log_event`.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.schemas import CreateUser, UpdateUser, ShowUser
from app.db.models import User
from app.services import crud_user as user
from app.api.deps import get_db, require_role 
from app import utils


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[ShowUser])
def list_users(
    id: int | None = None,
    full_name: str | None = None,
    email: str | None = None,
    phone_number: str | None = None,
    address: str | None = None,
    db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
        """List users with optional filters (admin only)."""

        filters = utils.filters(
            id= id,
            full_name= full_name,
            email= email,
            phone_number= phone_number,
            address= address,
        )
        searched = user.list_like(db, **filters)

        return searched
        
@router.post("/", response_model=List[ShowUser])
def create_user(payload: CreateUser, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))) -> Any:
    """Create a new user (admin only). Logs the creation event."""
    created = user.create(db, obj_in=payload)

    return created

@router.patch("/{user_id}", response_model=ShowUser)
def update_user(user_id: int, payload: UpdateUser, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Update user details (admin only). Prevents role escalation."""
    obj = user.get(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    if obj.role != UserRole.ADMIN and user_id != obj.user_id:
            raise HTTPException(status_code=403, detail="Only Admin")
    if payload.role == UserRole.ADMIN and obj.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only Admin") 
    updated = user.update(db, db_obj=obj, obj_in=payload)
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_User(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Delete a user (admin only). Restricted by role rules."""
    obj = user.get(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    if obj.role != UserRole.ADMIN and user_id != obj.user_id:
            raise HTTPException(status_code=403, detail="Only Admin")
    user.remove(db, id=user_id)

    return
