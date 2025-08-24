"""
Books Router
------------

This file defines the API endpo@router.patch("/{book_id}", response_model=ShowBook)
def update_book(book_id: int, payload: UpdateBook, db: Session = Depends(get_db), current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))):
    """Update an existing book's details (admin/librarian only). Logs the update event."""s for managing books in the library system.

Endpoints:
- GET /books/        → List books with optional filters (id, title, author, year, genre, copies)
- POST /books/       → Create a new book (admin/librarian only)
- PATCH /books/{id}  → Update book details (admin/librarian only)
- DELETE /books/{id} → Delete a book (admin/librarian only)

Notes:
- Admin/librarian actions require authentication and role checks.
- Each action logs an event with `log_event`.
- Database sessions are provided via `Depends(get_db)`.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.schemas import CreateBook, UpdateBook, ShowBook
from app.db.models import Book, User
from app.services import crud_book as book, log_event
from app.api.deps import get_db, require_roles
from app import utils


router = APIRouter(
    prefix="/books",
    tags=['Books']
)

@router.get("/", response_model=List[ShowBook])
def list_books(
    id: int | None = None,
    title: str | None = None,
    author: str | None = None,
    published_year: str | None = None,
    genre: str | None = None,
    total_copies: int | None = None,
    db: Session = Depends(get_db),):
    """List books with optional filters. Logs a search event."""

    filters = utils.filters(
        id= id,
        title= title,
        author= author,
        published_year= published_year,
        genre= genre,
        total_copies= total_copies
    )
    
    searched = book.list_like(db, **filters)
    return searched

@router.post("/", response_model=ShowBook)
def create_book(payload: CreateBook, db: Session = Depends(get_db), current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))):
    """Create a new book (admin/librarian only). Logs the creation event."""
    
    created = book.create(db, db_obj=book, obj_in=payload)
    return created

@router.patch("/{book_id}", response_model=ShowBook)
def update_book(book_id: int, payload: UpdateBook, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Update an existing book’s details (admin only). Logs the update event."""

    obj = book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    updated = book.update(db, db_obj=obj, obj_in=payload)
    return updated
    

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Delete a book by ID (admin only). Logs the deletion event."""
    
    obj = book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    
    Book.remove(db, id=book_id)
    return
