from .users import ShowUser, CreateUser, UpdateUser, SignupUser
from .books import ShowBook, CreateBook, UpdateBook
from .loans import ShowLoan, CreateLoan, UpdateLoan
from .events import ShowEvent, EventBase
from .token import Token, TokenPayload

__all__ = [
    "ShowUser", "CreateUser", "UpdateUser", "SignupUser",
    "ShowBook", "CreateBook", "UpdateBook",
    "ShowLoan", "CreateLoan", "UpdateLoan",
    "ShowEvent", "EventBase",
    "Token", "TokenPayload",
]

"""
Schemas package.

This package defines all Pydantic models used for data validation and 
serialization throughout the project. Each module groups related schemas 
(e.g., books, users, loans).

Conventions:
- `Base` classes hold shared fields.
- `Create` schemas are used for POST (all required).
- `Update` schemas are used for PATCH (all optional).
- `Show` schemas are returned in API responses (usually include IDs or relations).
"""


#TODO: Order
#TODO: define constraints (Pydantic) for critical fields