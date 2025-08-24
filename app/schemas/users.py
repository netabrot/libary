from datetime import date

from pydantic import BaseModel, EmailStr, SecretStr, Field, ConfigDict

from app.core.enums import UserRole
from .events import ShowEvent
from .loans import ShowLoan


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


class SignupUser(BaseModel):
    """Body for POST /auth/signup (self-registration)"""
    full_name: str
    email: EmailStr
    phone_number: str
    password: SecretStr
    address: str | None = None


class UpdateUser(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    join_date: date | None = None
    address: str | None = None
    password: SecretStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class ShowUser(UserBase):
    """Response shape for GET/POST responses"""
    id: int
    loans: list[ShowLoan] = Field(default_factory=list)
    events: list[ShowEvent] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
