from app.services.base import CRUDBase
from app.db.models.models import User
from app.schemas.schemas import CreateUser, UpdateUser
from app.core import security

class CRUDuser(CRUDBase[User, CreateUser, UpdateUser]):
    def update(self, db, *, db_obj: User, obj_in: UpdateUser | dict) -> User:
        if not isinstance(obj_in, dict):
            obj_in = obj_in.model_dump(exclude_unset=True)
        if "password" in obj_in and obj_in["password"] is not None:
            plain = obj_in["password"].get_secret_value()
            db_obj.password = security.get_password_hash(plain)
            obj_in.pop("password", None)
        for k, v in obj_in.items():
            setattr(db_obj, k, v)
        db.add(db_obj); db.commit(); db.refresh(db_obj)
        return db_obj

crud_user = CRUDuser(User)

