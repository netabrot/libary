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
    LIBRARIAN = "librarian"
    MEMBER = "member"


class ObjectType(str, Enum):
    USER = "user"
    BOOK = "book"
    LOAN = "loan"


class OrderStatus(str, Enum):
    WAITING = "waiting"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
