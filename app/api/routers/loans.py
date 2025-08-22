"""
Loans Router
------------

This file defines the API endpoints for managing book loans in the library system.

Endpoints:
- GET /loans/         → List loans with optional filters (book_id, member_id, borrow/return dates)
- POST /loans/        → Create a new loan (admin only, checks book availability)
- PATCH /loans/{id}   → Update loan details (admin only)
- DELETE /loans/{id}  → Delete a loan (admin only)

Notes:
- Admin-only actions require authentication and role checks.
- Each action logs an event with `log_event`.
- Database sessions are provided via `Depends(get_db)`.
"""

from datetime import date
from typing import List


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import EventType, ObjectType, UserRole
from app.schemas import CreateLoan, UpdateLoan, ShowLoan
from app.db.models import Book, User
from app.services import crud_loan as loan, log_event
from app.api.deps import get_db, require_role, TimedRoute
from app import utils

router = APIRouter(
    prefix="/loans",
    tags=['Loans']
)
router.route_class = TimedRoute

@router.get("/", response_model=List[ShowLoan])
def list_loans(
        book_id: int | None = None,
        borrow_date: date | None = None,
        due_date: date | None = None,
        member_id: int | None = None,
        return_date: date | None = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(UserRole.ADMIN))):
    """List loans with optional filters (admin only)."""

    
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
    """Create a new loan (admin only). Checks book availability and logs the event."""
    book = db.query(Book).filter(Book.id == payload.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies <= 0:
        log_event(db, EventType.LOAN_FAILED, ObjectType.LOAN, current_user, status_code=status.HTTP_400_BAD_REQUEST, method="POST",book_id=payload.book_id)
        raise HTTPException(status_code=400, detail="No available copies for this book")
    created = loan.create(db, obj_in=payload)

    log_event(db, EventType.LOAN_CREATED, ObjectType.LOAN, current_user, status_code=status.HTTP_201_CREATED, method="POST",loan_id=created.id, book_id=payload.book_id)
    return created

@router.patch("/{loan_id}", response_model=ShowLoan)
def update_loan(loan_id: int, payload: UpdateLoan, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Update loan details (admin only). Logs updated fields."""

    obj = loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    updated = loan.update(db, db_obj=obj, obj_in=payload)
    log_event(db, EventType.LOAN_UPDATED, ObjectType.LOAN, current_user, status_code=status.HTTP_202_ACCEPTED, method="PATCH", book_id=updated.book_id,updated_fields=utils.changed_fields(payload))
    return updated
    

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Delete a loan by ID (admin only). Logs the deletion event."""
    obj = loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan.remove(db, id=loan_id)
    log_event(db, EventType.LOAN_DELETED, ObjectType.LOAN, current_user, status_code=status.HTTP_204_NO_CONTENT, method="DELETE", loan_id=loan_id, book_id=obj.book_id)

    return