from __future__ import annotations

from datetime import date, datetime
from typing import Any
from pydantic import BaseModel,EmailStr, SecretStr, Field, ConfigDict

class MemberBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    join_date: date | None = None
    address: str | None = None
    admin: bool

class CreateMember(MemberBase):
    """Body for POST /members"""
    password: SecretStr

class UpdateMember(BaseModel):
    full_name: str| None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    join_date: date | None = None
    address: str | None = None
    password_hash: SecretStr |  None = None
    admin: bool | None = None

class ShowMember(MemberBase):
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
    available_copies: int 

class CreateBook(BookBase):
    pass

class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    published_year: int | None = None
    genre: str | None = None
    available_copies: int | None = None

class ShowBook(BookBase):
    id: int
    loans: list[ShowLoan] = Field(default_factory=list) 
    model_config = ConfigDict(from_attributes=True)


class LoanBase(BaseModel):
    book_id: int 
    borrow_date: date
    due_date: date
    return_date: date | None = None
    member_id: int 

class CreateLoan(LoanBase):
    pass

class UpdateLoan(BaseModel):
    book_id: int | None = None
    borrow_date: date | None = None
    due_date: date | None = None
    return_date: date | None = None
    member_id: int | None = None

class ShowLoan(LoanBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class EventBase(BaseModel):
    time_stamp: datetime
    event_type: str
    meta_data: dict[str, Any] | None = None
    member_id: int | None = None

class CreateEvent(EventBase):
    pass

class ShowEvent(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


ShowMember.model_rebuild()
ShowBook.model_rebuild()
ShowLoan.model_rebuild()
ShowEvent.model_rebuild()


#TODO: Order
#TODO: define constraints (Pydantic) for critical fields