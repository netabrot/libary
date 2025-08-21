from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schemas import CreateBook, UpdateBook, ShowBook
from app.services.book import crud_book as book
from app.api.deps import require_role
from app.db.models.models import Book, User
from app.core.enums import UserRole

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
    db: Session = Depends(get_db)):
        
        return book.list_like(
            db,
            **{k: v for k, v in {
                id: int,
                title: str,
                author: str,
                published_year: str,
                genre: str,
                total_copies: int
            }.items() if v is not None}
        )

@router.post("/", response_model=ShowBook)
def create_book(payload: CreateBook, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    return book.create(db, db_obj=book, obj_in=payload)

@router.patch("/{book_id}", response_model=ShowBook)
def update_book(book_id: int, payload: UpdateBook, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.update(db, db_obj=obj, obj_in=payload)
    

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    if obj.role != UserRole.ADMIN and book_id != obj.book_id:
            raise HTTPException(status_code=403, detail="Only Admin")
    Book.remove(db, id=book_id)
    return
