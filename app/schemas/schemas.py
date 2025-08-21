from __future__ import annotations

from datetime import date, datetime
from typing import Any
from pydantic import BaseModel,EmailStr, SecretStr, Field, ConfigDict
from app.core.enums import *

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


class BookBase(BaseModel):

    title: str
    author: str
    published_year: int 
    genre: str | None = None
    total_copies: int 

class CreateBook(BookBase):
    pass

class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    published_year: int | None = None
    genre: str | None = None
    total_copies: int | None = None

class ShowBook(BookBase):
    id: int
    loans: list[ShowLoan] = Field(default_factory=list) 
    model_config = ConfigDict(from_attributes=True)


class LoanBase(BaseModel):
    book_id: int 
    borrow_date: date
    due_date: date
    return_date: date | None = None
    user_id: int 

class CreateLoan(LoanBase):
    pass

class UpdateLoan(BaseModel):
    book_id: int | None = None
    borrow_date: date | None = None
    due_date: date | None = None
    return_date: date | None = None
    user_id: int | None = None

class ShowLoan(LoanBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class EventBase(BaseModel):
    timestamp: datetime
    event_type: str
    meta_data: dict[str, Any] | None = None
    user_id: int | None = None

class CreateEvent(EventBase):
    pass

class ShowEvent(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


ShowUser.model_rebuild()
ShowBook.model_rebuild()
ShowLoan.model_rebuild()
ShowEvent.model_rebuild()


#TODO: Order
#TODO: define constraints (Pydantic) for critical fields