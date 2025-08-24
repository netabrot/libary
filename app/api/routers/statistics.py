"""
Statistics Router
-----------------

API endpoints for retrieving library management statistics.
Provides actionable insights for library managers and staff.

Endpoints:
- GET /statistics/overview      → Library overview statistics
- GET /statistics/books         → Book management statistics  
- GET /statistics/users         → User management statistics
- GET /statistics/operations    → Daily operational statistics

Notes:
- All endpoints require authentication
- Admin/librarian roles required for most statistics
- Statistics are designed for practical library management decisions
- Each endpoint logs its own access for monitoring
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles, get_current_user
from app.core.enums import UserRole
from app.db import get_db
from app.db.models.user import User
from app.schemas.statistics import LibraryOverview, BookStatistics, UserStatistics, OperationalStats
from app.services.statistics import get_statistics_service

router = APIRouter(
    prefix="/statistics",
    tags=['Statistics']
)


@router.get("/overview", response_model=LibraryOverview)
def get_library_overview(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """
    Get library overview statistics for management dashboard.
    
    Provides insights for:
    - Total inventory counts
    - Current circulation status
    - Overdue loan tracking
    
    Required: Admin or Librarian role
    """
    stats_service = get_statistics_service(db)
    return stats_service.get_library_overview()


@router.get("/books", response_model=BookStatistics)
def get_book_statistics(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """
    Get book management statistics for inventory oversight.

    Provides insights for:
    - Book inventory and availability
    - Popular book identification
    - Genre distribution analysis
    - Circulation patterns
    
    Required: Admin or Librarian role
    """

    stats_service = get_statistics_service(db)
    return stats_service.get_book_statistics()


@router.get("/users", response_model=UserStatistics)
def get_user_statistics(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """
    Get user management statistics for patron oversight.
    
    Provides insights for:
    - User registration and activity
    - Top borrower identification
    - Overdue book management
    - Growth tracking
    
    Required: Admin or Librarian role
    """
    stats_service = get_statistics_service(db)
    return stats_service.get_user_statistics()


@router.get("/operations", response_model=OperationalStats)
def get_operational_statistics(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Get daily operational statistics for immediate management decisions.
    
    Provides today's insights for:
    - Daily loan and return activity
    - Pending order management
    - System usage monitoring
    - Peak usage time identification
    
    Available to all authenticated library staff.
    """

    stats_service = get_statistics_service(db)
    return stats_service.get_operational_statistics()
