from typing import Dict, Any, List

from pydantic import BaseModel, ConfigDict


class StatisticsBase(BaseModel):
    """Base statistics schema following project conventions."""
    model_config = ConfigDict(extra="ignore")


class LibraryOverview(StatisticsBase):
    """Library overview statistics for management dashboard."""
    total_books: int
    total_users: int
    total_loans: int
    available_books: int
    books_on_loan: int
    overdue_loans: int

    model_config = ConfigDict(from_attributes=True)


class BookStatistics(StatisticsBase):
    """Book-related statistics for inventory management."""
    total_books: int
    books_by_genre: Dict[str, int]
    most_borrowed_books: List[Dict[str, Any]]
    available_books: int
    books_on_loan: int

    model_config = ConfigDict(from_attributes=True)


class UserStatistics(StatisticsBase):
    """User-related statistics for patron management."""
    total_users: int
    active_users: int
    new_users_this_month: int
    top_borrowers: List[Dict[str, Any]]
    users_with_overdue: int

    model_config = ConfigDict(from_attributes=True)


class OperationalStats(StatisticsBase):
    """Daily operational statistics for library management."""
    loans_today: int
    returns_today: int
    new_orders: int
    system_events_today: int

    model_config = ConfigDict(from_attributes=True)
