from .loans import ShowLoan
from .events import ShowEvent
from . import BaseModel, EmailStr, date, UserRole, SecretStr, Field, ConfigDict

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    join_date: date | None = None
    address: str | None = None
    role: UserRole
    is_active: bool

class CreateUser(UserBase):
    """Body for POST /users"""
    password: SecretStr

class UpdateUser(BaseModel):
    full_name: str| None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    join_date: date | None = None
    address: str | None = None
    password: SecretStr |  None = None
    role: UserRole | None = None
    is_active: bool | None = None

class ShowUser(UserBase):
    """Response shape for GET/POST responses"""
    id: int 
    loans: list[ShowLoan] = Field(default_factory=list)
    events: list[ShowEvent] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

