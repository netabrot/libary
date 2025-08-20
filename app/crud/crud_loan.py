from app.crud.base import CRUDBase
from app.models import Loan
from app.schemas import CreateLoan, UpdateLoan
from app.hashing import Hash


class CRUDLoan(CRUDBase[Loan, CreateLoan, UpdateLoan]):
    pass

crud_loan = CRUDLoan(Loan)

