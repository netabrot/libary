from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.books import CreateBook, UpdateBook, ShowBook
from app.services.book import crud_book as book
from app.api.deps import get_current_user, require_role
from app.db.models.book import Book
from app.db.models.user import User
from app.core.enums import UserRole
from app.services.event import log_event
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
        
    filters = utils.filters(
        id= id,
        title= title,
        author= author,
        published_year= published_year,
        genre= genre,
        total_copies= total_copies
    )
    
    searched = book.list_like(db, **filters)
    log_event(db,"book.searched", **filters)
    return searched

@router.post("/", response_model=ShowBook)
def create_book(payload: CreateBook, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    created = book.create(db, db_obj=book, obj_in=payload)
    log_event(db,"book.created", current_user, book_id=created.id)
    return created

@router.patch("/{book_id}", response_model=ShowBook)
def update_book(book_id: int, payload: UpdateBook, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated = book.update(db, db_obj=obj, obj_in=payload)
    log_event(db,"book.updated",current_user, book_id,  updated_fields=utils.changed_fields(payload))
    return updated
    

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    
    Book.remove(db, id=book_id)

    log_event(db,"book.deleted",current_user, book_id)

    return
