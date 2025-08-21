from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.loans import CreateLoan, UpdateLoan, ShowLoan
from app.db.models.models import Book, User
from app.services.loan import crud_loan as loan
from app.api.deps import require_role
from app.core.enums import UserRole
from app.services.event import log_event
from app import utils



router = APIRouter(
    prefix="/loans",
    tags=['Loans']
)

@router.get("/", response_model=List[ShowLoan])
def list_loans(
        book_id: int | None = None,
        borrow_date: date | None = None,
        due_date: date | None = None,
        member_id: int | None = None,
        return_date: date | None = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(UserRole.ADMIN))):
    
    filters = utils.filters(
        book_id=book_id,
        borrow_date=borrow_date,
        due_date=due_date,
        member_id=member_id,
        return_date=return_date,
    )
   
    searched = loan.list_like(db, **filters)
        
    return searched

@router.post("/", response_model=ShowLoan, status_code=status.HTTP_201_CREATED)
def create_loan(payload: CreateLoan, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    book = db.query(Book).filter(Book.id == payload.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies <= 0:
        log_event(db, "loan.failed",current_user, reason="book_not_found", book_id=payload.book_id)
        raise HTTPException(status_code=400, detail="No available copies for this book")
    created = loan.create(db, obj_in=payload)

    log_event(db, "loan.created", current_user, loan_id=created.id, book_id=payload.book_id)
    return created

@router.patch("/{loan_id}", response_model=ShowLoan)
def update_loan(loan_id: int, payload: UpdateLoan, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    updated = loan.update(db, db_obj=obj, obj_in=payload)
    log_event(db, "loan.updated", current_user, loan_id=loan_id, book_id=updated.book_id,updated_fields=utils.changed_fields(payload))

    return updated
    

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    obj = loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan.remove(db, id=loan_id)
    log_event(db, "loan.deleted", current_user, loan_id=loan_id, book_id=obj.book_id)
    return