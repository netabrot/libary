from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"