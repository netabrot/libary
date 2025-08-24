"""
Service layer: contains CRUD wrappers and business logic
for users, books, loans, events, and authentication.
"""


from . import auth
from .user import crud_user
from .book import crud_book
from .loan import crud_loan
from .order import crud_order
from .event import log_event

__all__ = ["login", "crud_user", "crud_book", "crud_loan", "crud_order","log_event"]

