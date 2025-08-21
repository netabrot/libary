from app.services.base import CRUDBase
from app.db.models.models import Book
from app.schemas.schemas import CreateBook, UpdateBook

class CRUDbook(CRUDBase[Book, CreateBook, UpdateBook]):
    def available_copies(self):
        active_loans = [loan for loan in self.loans if loan.return_date is None]
        return self.total_copies - len(active_loans)

crud_book = CRUDbook(Book)

