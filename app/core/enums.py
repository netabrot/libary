"""
Enums
-----

Centralized enumerations for roles and other constants.

UserRole:
- ADMIN  → full privileges
- MEMBER → normal user
"""

from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"

class EventType(str, Enum):
    HTTP_COMPLETED = "http.request.completed"
    USER_CREATED   = "user.created"
    USER_LOGGED_IN = "user.logged_in"
    USER_REMOVED   = "user.removed"
    USER_UPDATED   = "user.updated"

    BOOK_SEARCHED  = "book.searched"
    BOOK_UPDATED   = "book.updated"
    BOOK_DELETED   = "book.deleted"
    BOOK_CREATED  = "book.created"

    LOAN_CREATED   = "loan.created"
    LOAN_UPDATED   = "loan.updated"
    LOAN_DELETED   = "loan.deleted"
    LOAN_FAILED    = "loan.failed"

class ObjectType(str, Enum):
    USER = "user"
    BOOK = "book"
    LOAN = "loan"