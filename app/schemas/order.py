from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import OrderStatus


class BookOrderBase(BaseModel):
    book_title: str
    priority: int
    status: OrderStatus = OrderStatus.WAITING


class CreateBookOrder(BookOrderBase):
    pass


class ShowBookOrder(BaseModel):
    id: int
    user_id: int
    book_id: int
    book_title: str
    order_date: datetime
    priority: int
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)
