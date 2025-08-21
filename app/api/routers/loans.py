from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schemas import CreateLoan, UpdateLoan, ShowLoan
from app.crud.crud_loan import crud_loan

router = APIRouter(
    prefix="/loans",
    tags=['Loans']
)

@router.get("/", response_model=List[ShowLoan])
def list_Loans(
        book_id: int,
        borrow_date: date | None = None,
        due_date: date | None = None,
        member_id: int | None = None,
        return_date: date | None = None,
        db: Session = Depends(get_db),
):
        return crud_loan.list_like(
            db,
            **{k: v for k, v in {
                "book_id": book_id,
                "borrow_date": borrow_date,
                "due_date": due_date,
                "member_id": member_id,
                "return_date": return_date,
            }.items() if v is not None}
        )

@router.post("/", response_model=ShowLoan, status_code=status.HTTP_201_CREATED)
def create_loan(payload: CreateLoan, db: Session = Depends(get_db)):
    return crud_loan.create(db, obj_in=payload)

@router.patch("/{loan_id}", response_model=ShowLoan)
def update_loan(loan_id: int, payload: UpdateLoan, db: Session = Depends(get_db)):
    obj = crud_loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    return crud_loan.update(db, db_obj=obj, obj_in=payload)

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    obj = crud_loan.get(db, id=loan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Loan not found")
    crud_loan.remove(db, id=loan_id)
    return