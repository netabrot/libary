from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Member
from app.schemas import CreateMember, UpdateMember, ShowMember


class CRUDMember(CRUDBase[Member, CreateMember, UpdateMember,ShowMember ]):
    def get_by_id(self, db: Session, *, id: int) -> Optional[ShowMember]:
        return db.query(Member).filter(Member.id == id).first()
    
    def get_by_name(self, db: Session, *, full_name: str) -> Optional[ShowMember]:
        return db.query(Member).filter(Member.full_name == full_name).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[ShowMember]:
        return db.query(Member).filter(Member.email == email).first()
    
    def get_by_phone_number(self, db: Session, *, phone_number: str) -> Optional[ShowMember]:
        return db.query(Member).filter(Member.phone_number == phone_number).first()

    def get_by_name(self, db: Session, *, full_name: str) -> Optional[list[ShowMember]]:
        return db.query(Member).filter(Member.full_name == full_name).first()

    def get_by_join_date(self, db: Session, *, join_date: date) -> Optional[list[ShowMember]]:
        return db.query(Member).filter(Member.join_date == join_date).first()

    def get_by_address(self, db: Session, *, address: str) -> Optional[list[ShowMember]]:
        return db.query(Member).filter(Member.address == address).first()

    def update(
        self, db: Session, *, db_obj: Member, obj_in: Union[UpdateMember, Dict[str, Any]]
    ) -> Member:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_admin(self, Member: Member) -> bool:
        return Member.is_admin


Member = CRUDMember(Member)