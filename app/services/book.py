from typing import List, Optional

from sqlalchemy import and_
from app.services.base import CRUDBase
from app.db.models.book import Book
from app.schemas.books import CreateBook, UpdateBook
from sqlalchemy.orm import Session


class CRUDbook(CRUDBase[Book, CreateBook, UpdateBook]):
    def get_available(self, db: Session) -> List[Book]:
        """Get books that are available for checkout."""
        return db.query(Book).filter(Book.available_copies > 0).all()
    
    def update_availability(self, db: Session, book_id: int, change: int) -> Optional[Book]:
        """Update book availability (positive=return, negative=checkout)."""
        book = self.get(db, book_id)
        if book:
            new_available = book.available_copies + change
            if 0 <= new_available <= book.total_copies:
                book.available_copies = new_available
                db.commit()
                db.refresh(book)
        return book

crud_book = CRUDbook(Book)

