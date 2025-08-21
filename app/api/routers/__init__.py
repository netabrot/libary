from .users import router as users_router
from .books import router as books_router
from .loans import router as loans_router
from .auth import router as auth_router

__all__ = [
    "users_router",
    "books_router",
    "loans_router",
    "auth_router",
]
