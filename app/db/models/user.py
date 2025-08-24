from datetime import date

from sqlalchemy import Column, Integer, String, Date, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.core.enums import UserRole
from app.db import Base

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
    is_active = Column(Boolean, default=True)

    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    book_orders = relationship("BookOrder", back_populates="user", cascade="all, delete-orphan")
