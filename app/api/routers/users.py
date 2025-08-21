from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schemas import CreateUser, UpdateUser, ShowUser
from app.services.user import crud_user as user

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[ShowUser])
def list_users(
    id: str | None = None,
    full_name: str | None = None,
    email: str | None = None,
    phone_number: str | None = None,
    address: str | None = None,
    db: Session = Depends(get_db),
):
        return user.list_like(
            db,
            **{k: v for k, v in {
                "id": id,
                "full_name": full_name,
                "email": email,
                "phone_number": phone_number,
                "address": address,
            }.items() if v is not None}
        )

@router.patch("/{user_id}", response_model=ShowUser)
def update_User(user_id: int, payload: UpdateUser, db: Session = Depends(get_db)):
    obj = user.get(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user.update(db, db_obj=obj, obj_in=payload)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_User(user_id: int, db: Session = Depends(get_db)):
    obj = user.get(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    user.remove(db, id=user_id)
    return
