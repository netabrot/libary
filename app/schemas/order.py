from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field

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
    order_date: datetime
    priority: int
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)
