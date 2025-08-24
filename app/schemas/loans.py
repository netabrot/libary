from datetime import date
from pydantic import BaseModel, ConfigDict

class LoanBase(BaseModel):
    book_id: int 
    borrow_date: date
    due_date: date
    return_date: date | None = None
    user_id: int 

class CreateLoan(LoanBase):
    pass

class UpdateLoan(BaseModel):
    book_id: int | None = None
    borrow_date: date | None = None
    due_date: date | None = None
    return_date: date | None = None
    user_id: int | None = None

class ShowLoan(LoanBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PublicLoan(BaseModel):
    """Loan information without user_id for public book display."""
    id: int
    book_id: int
    borrow_date: date
    due_date: date
    return_date: date | None = None
    model_config = ConfigDict(from_attributes=True)