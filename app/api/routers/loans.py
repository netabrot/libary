"""
Loans Router
------------

This file defines the API endpoints for managing book loans in the library system.

Endpoints:
- GET /loans/         → List loans with optional filters (book_id, member_id, borrow/return dates)
- POST /loans/        → Create a new loan (admin only, checks book availability)
- GET /loans/active   → Get active loan for a user/book combination
- PATCH /loans/return/{id} → Return a book by loan ID
- PATCH /loans/{id}   → Update loan details (admin only)
- DELETE /loans/{id}  → Delete a loan (admin only)

Notes:
- Admin-only actions require authentication and role checks.
- Database sessions are provided via `Depends(get_db)`.
"""

from datetime import date
from typing import List


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.schemas import CreateLoan, UpdateLoan, ShowLoan
from app.db.models import Book, User
from app.services import crud_loan as loan
from app.api.deps import get_db, require_role
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
    """Create a new loan (admin only). Checks book availability."""
    created = loan.create_checkout(db, obj_in=payload)
    return created

@router.patch("/return/{loan_id}", response_model=ShowLoan)
def return_book(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Return a book by loan ID."""
    obj = loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan.return_book(db, obj_in=obj)

@router.get("/active", response_model=ShowLoan)
def get_active_loan(book_id: int, member_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Get active loan for a user/book combination."""
    active_loan = loan.get_active_loan(db, book_id=book_id, member_id=member_id)
    if not active_loan:
        raise HTTPException(status_code=404, detail="No active loan found")
    return active_loan

@router.patch("/{loan_id}", response_model=ShowLoan)
def update_loan(loan_id: int, payload: UpdateLoan, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Update loan details (admin only)."""
    obj = loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    updated = loan.update(db, db_obj=obj, obj_in=payload)
    return updated

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Delete a loan by ID (admin only)."""
    obj = loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan.remove(db, id=loan_id)
    return