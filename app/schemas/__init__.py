from .users import ShowUser, CreateUser, UpdateUser, SignupUser
from .books import ShowBook, CreateBook, UpdateBook
from .loans import ShowLoan, CreateLoan, UpdateLoan, PublicLoan
from .events import ShowEvent, EventBase
from .order import CreateBookOrder, ShowBookOrder
from .token import Token, TokenPayload
from .statistics import LibraryOverview, BookStatistics, UserStatistics, OperationalStats

__all__ = [
    "ShowUser", "CreateUser", "UpdateUser", "SignupUser",
    "ShowBook", "CreateBook", "UpdateBook",
    "ShowLoan", "CreateLoan", "UpdateLoan", "PublicLoan",
    "ShowEvent", "EventBase",
    "CreateBookOrder", "ShowBookOrder",
    "Token", "TokenPayload",
    "LibraryOverview", "BookStatistics", "UserStatistics", "OperationalStats",
]

"""
Schemas package.

This package defines all Pydantic models used for data validation and 
serialization throughout the project. Each module groups related schemas 
(e.g., books, users, loans).

Conventions:
- `Base` classes hold shared fields.
- `Create` schemas are used for POST (all required).
- `Update` schemas are used for PUT (all optional).
- `Show` schemas are returned in API responses (usually include IDs or relations).
"""


