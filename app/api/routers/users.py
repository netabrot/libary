from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.users import CreateUser, UpdateUser, ShowUser
from app.services.user import crud_user as user
from app.api.deps import require_role
from app.db.models.user import User
from app.core.enums import UserRole
from app.services.event import log_event
from app import utils
from app.api.deps import get_db

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
    created = user.create(db, obj_in=payload)
    log_event(db, "user.created",current_user, user_id=created.id)
    return created

@router.patch("/{user_id}", response_model=ShowUser)
def update_user(user_id: int, payload: UpdateUser, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = user.get(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    if obj.role != UserRole.ADMIN and user_id != obj.user_id:
            raise HTTPException(status_code=403, detail="Only Admin")
    if payload.role == UserRole.ADMIN and obj.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only Admin") 
    updated = user.update(db, db_obj=obj, obj_in=payload)
    log_event(db,"user.updated",current_user, user_id, updated_fields=utils.changed_fields(payload))
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_User(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = user.get(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    if obj.role != UserRole.ADMIN and user_id != obj.user_id:
            raise HTTPException(status_code=403, detail="Only Admin")
    user.remove(db, id=user_id)
    log_event(db,"user.removed",current_user, user_id)

    return
