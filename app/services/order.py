from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.services.base import CRUDBase
from app.db.models.order import BookOrder
from app.db.models.book import Book
from app.schemas.order import CreateBookOrder, ShowBookOrder
from app.core.enums import OrderStatus
from . import crud_book

class CRUDOrder(CRUDBase[BookOrder, CreateBookOrder, ShowBookOrder]):
    def get_user_orders(self, db: Session, user_id: int) -> List[BookOrder]:
        """Get all orders for a specific user."""
        return db.query(self.model).filter(self.model.user_id == user_id).order_by(desc(self.model.order_date)).all()
    
    def get_waiting_orders_by_book(self, db: Session, book_id: int) -> List[BookOrder]:
        """Get waiting orders for a specific book, ordered by priority and date."""
        return db.query(self.model).filter(self.model.book_id == book_id,self.model.status == OrderStatus.WAITING).order_by(
            desc(self.model.priority),self.model.order_date).all()
    
    def get_user_order_for_book(self, db: Session, user_id: int, book_id: int) -> Optional[BookOrder]:
        """Check if user has an active order for a specific book."""
        return db.query(self.model).filter(self.model.user_id == user_id,self.model.book_id
                                            == book_id,self.model.status == OrderStatus.WAITING).first()
    
    def create_order_by_title(self, db: Session, *, user_id: int, book_title: str) -> BookOrder:
        """Create a new order by searching for book title."""
        book = crud_book.list_like(db, title=book_title)
        book = book[0] if book else None
        
        if not book:
            raise ValueError(f"Book with title '{book_title}' not found")
        
        if book.available_copies > 0:
            raise ValueError(f"Book '{book.title}' is currently available for checkout")
        
        existing_order = self.get_user_order_for_book(db, user_id, book.id)
        if existing_order:
            raise ValueError(f"You already have an active order for '{book.title}'")
        
        order_data = {
            "user_id": user_id,
            "book_id": book.id,
            "priority": 1,
            "status": OrderStatus.WAITING
        }
        
        db_obj = self.model(**order_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def cancel_order(self, db: Session, *, order_id: int, user_id: int) -> BookOrder:
        """Cancel a user's order."""
        order = db.query(self.model).filter(
            self.model.id == order_id,
            self.model.user_id == user_id
        ).first()
        
        if not order:
            raise ValueError("Order not found")
        
        if order.status != OrderStatus.WAITING:
            raise ValueError("Can only cancel waiting orders")
        
        order.status = OrderStatus.CANCELLED
        db.commit()
        db.refresh(order)
        return order

crud_order = CRUDOrder(BookOrder)
