from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class MemberBase(BaseModel):
    full_name: str
    email: str
    phone_number: str
    join_date: date | None = None
    address: str | None = None

class CreateMember(MemberBase):
    """Body for POST /events"""
    pass

class ShowMember(MemberBase):
    """Response shape for GET/POST responses"""
    id: int 
    loans: list["ShowLoan"] = Field(default_factory=list) 
    events: list["ShowEvent"] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):

    title: str
    author: str
    published_year: int 
    genre: str | None = None
    available_copies: int 

class CreateBook(BookBase):
    pass

class ShowBook(BookBase):
    id: int
    loans: list[ShowLoan] = Field(default_factory=list) 
    model_config = ConfigDict(from_attributes=True)


class LoanBase(BaseModel):
    book_id: int 
    borrow_date: date
    return_date: date | None = None
    member_id: int 

class CreateLoan(LoanBase):
    pass

class ShowLoan(LoanBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class EventBase(BaseModel):
    time_stamp = date | None = None
    event_type: str
    metadata: str | None = None
    member_id: int | None = None

class CreateEvent(EventBase):
    pass

class ShowEvent(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


#TODO: Order