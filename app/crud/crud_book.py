from app.crud.base import CRUDBase
from app.models import Book
from app.schemas import CreateBook, UpdateBook
from app.hashing import Hash


class CRUDBook(CRUDBase[Book, CreateBook, UpdateBook]):
    pass

crud_Book = CRUDBook(Book)

