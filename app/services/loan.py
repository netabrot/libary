from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.services.base import CRUDBase
from app.db.models.loan import Loan
from app.schemas.loans import CreateLoan, UpdateLoan
from datetime import date, timedelta
from . import crud_book

class CRUDloan(CRUDBase[Loan, CreateLoan, UpdateLoan]):
    def create_checkout(self, db: Session, *, user_id: int, book_id: int, loan_month: int = 1) -> Optional[Loan]:
        """Create a new loan"""
        book = crud_book.get(db, book_id)
        if not book or book.available_copies <= 0:
            return None
        
        existing = self.get_active_loan(db, user_id=user_id, book_id=book_id)
        if existing:
            return None
        
        due_date = date.today() + timedelta(days=loan_month)
        loan = Loan(user_id=user_id,book_id=book_id,due_date=due_date)
        db.add(loan)
        
        crud_book.update_availability(db, book_id, -1)
        
        db.commit()
        db.refresh(loan)
        return loan
    
    def return_book(self, db: Session, loan_id: int) -> Optional[Loan]:
        """Return a book."""
        loan = self.get(db, loan_id)
        if not loan or loan.return_date is not None:
            return None
        
        loan.return_date = date.today()
        crud_book.update_availability(db, loan.book_id, 1)
        db.commit()
        db.refresh(loan)
        return loan
    
    def get_active_loan(self, db: Session, *, user_id: int, book_id: int) -> Optional[Loan]:
        """Get active loan for a user/book combination."""
        return db.query(Loan).filter(
            and_(
                Loan.user_id == user_id,
                Loan.book_id == book_id,
                Loan.return_date == None
            )
        ).first()
    
    def get_user_loans(self, db: Session, user_id: int, active_only: bool = False) -> List[Loan]:
        """Get all loans for a user."""
        query = db.query(Loan).filter(Loan.user_id == user_id)
        if active_only:
            query = query.filter(Loan.return_date == None)
        return query.order_by(Loan.borrow_date.desc()).all()

crud_loan = CRUDloan(Loan)
