from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CreateMember, UpdateMember, ShowMember
from app.crud.crud_member import crud_member

router = APIRouter(
    prefix="/members",
    tags=['Members']
)

@router.get("/", response_model=List[ShowMember])
def list_members(
    id: str | None = None,
    full_name: str | None = None,
    email: str | None = None,
    phone_number: str | None = None,
    address: str | None = None,
    db: Session = Depends(get_db),
):
        return crud_member.list_like(
            db,
            **{k: v for k, v in {
                "id": id,
                "full_name": full_name,
                "email": email,
                "phone_number": phone_number,
                "address": address,
            }.items() if v is not None}
        )

@router.post("/", response_model=ShowMember, status_code=status.HTTP_201_CREATED)
def create_member(payload: CreateMember, db: Session = Depends(get_db)):
    if payload.email and crud_member.get_by(db, email=str(payload.email)):
        raise HTTPException(status_code=400, detail="Email already exists")
    if payload.phone_number and crud_member.get_by(db, phone_number=str(payload.phone_number)):
        raise HTTPException(status_code=400, detail="Phone_number already exists")
    return crud_member.create(db, obj_in=payload)

@router.patch("/{member_id}", response_model=ShowMember)
def update_member(member_id: int, payload: UpdateMember, db: Session = Depends(get_db)):
    obj = crud_member.get(db, member_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud_member.update(db, db_obj=obj, obj_in=payload)

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    obj = crud_member.get(db, member_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Member not found")
    crud_member.remove(db, id=member_id)
    return
