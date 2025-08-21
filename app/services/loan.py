from app.services.base import CRUDBase
from app.db.models.loan import Loan
from app.schemas.loans import CreateLoan, UpdateLoan
from datetime import date

class CRUDloan(CRUDBase[Loan, CreateLoan, UpdateLoan]):
    def calculate_return_date(self):
        return date.today - self.borrow_date

crud_loan = CRUDloan(Loan)
