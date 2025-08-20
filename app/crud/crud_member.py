from app.crud.base import CRUDBase
from app.models import Member
from app.schemas import CreateMember, UpdateMember
from app.hashing import Hash


class CRUDMember(CRUDBase[Member, CreateMember, UpdateMember]):
    def create(self, db, *, obj_in: CreateMember) -> Member:
        data = obj_in.model_dump(exclude={"password"})      
        plain = obj_in.password.get_secret_value()
        hashed = Hash.get_password_hash(plain)
        db_obj = Member(**data, password=hashed)
        db.add(db_obj); db.commit(); db.refresh(db_obj)
        return db_obj

    def update(self, db, *, db_obj: Member, obj_in: UpdateMember | dict) -> Member:
        if not isinstance(obj_in, dict):
            obj_in = obj_in.model_dump(exclude_unset=True)
        if "password" in obj_in and obj_in["password"] is not None:
            plain = obj_in["password"].get_secret_value()
            db_obj.password = Hash.get_password_hash(plain)
            obj_in.pop("password", None)
        for k, v in obj_in.items():
            setattr(db_obj, k, v)
        db.add(db_obj); db.commit(); db.refresh(db_obj)
        return db_obj

    def is_admin(self, Member: Member) -> bool:
        return Member.is_admin

crud_member = CRUDMember(Member)

