from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, func
from sqlalchemy.orm import relationship

from app.core.enums import OrderStatus
from app.db import Base


class BookOrder(Base):
    """Book order/waiting list for unavailable books."""
    __tablename__ = 'book_orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    order_date = Column(DateTime(timezone=True), default=func.now())
    priority = Column(Integer, default=1)
    status = Column(SAEnum(OrderStatus), default=OrderStatus.WAITING)

    notify_when_available = Column(String, default="email")

    user = relationship("User", back_populates="book_orders")
    book = relationship("Book", back_populates="orders")
