# Models = database tables.

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Date, Text, func, text, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import date
from app.core.enums import *

class User(Base):
    """Library User: a registered user who can borrow books."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    join_date = Column(Date, default=date.today)
    address = Column(String)
    password = Column(String)
    role = Column(SAEnum(UserRole), default=UserRole.MEMBER)
    is_active = Column(Boolean, default=False)

    loans = relationship("Loan", back_populates="User", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="User", cascade="all, delete-orphan")


class Book(Base):
    """Book item in the library catalog."""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_year = Column(Integer, index=True)
    genre = Column(String)
    available_copies = Column(Integer,nullable=False, default=1, server_default=text("1"))

    loans = relationship("Loan", back_populates="book", cascade="all, delete-orphan")


class Loan(Base):
    """A loan record: which User borrowed which book and when."""

    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False)
    borrow_date = Column(Date, nullable=False, default=date.today)
    due_date = Column(Date, nullable=False, default=date.today)
    return_date = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    User = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")

class Event(Base):
    """System log/event: what happened and when (optionally linked to a User)."""

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    event_type = Column(String, index=True)
    meta_data = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    User = relationship("User", back_populates="events")


#TODO: Order
