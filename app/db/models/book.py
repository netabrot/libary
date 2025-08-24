from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import relationship

from app.db import Base

class Book(Base):
    """Book item in the library catalog."""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_year = Column(Integer, index=True)
    genre = Column(String)
    total_copies = Column(Integer,nullable=False, default=1, server_default=text("1"))
    available_copies = Column(Integer,nullable=False, default=1, server_default=text("1"))

    loans = relationship("Loan", back_populates="book", cascade="all, delete-orphan")
    orders = relationship("BookOrder", back_populates="book", cascade="all, delete-orphan")