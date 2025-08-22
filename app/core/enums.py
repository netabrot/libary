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