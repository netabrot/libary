"""
Service layer: contains CRUD wrappers and business logic
for users, books, loans, events, statistics, and authentication.
"""

from . import auth
from .book import crud_book
from .event import log_event
from .loan import crud_loan
from .order import crud_order
from .statistics import get_statistics_service
from .user import crud_user

__all__ = ["login", "crud_user", "crud_book", "crud_loan", "crud_order", "log_event", "get_statistics_service"]
