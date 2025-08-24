"""
Statistics Service
-----------------

Service layer for generating library management statistics.
Follows Single Responsibility Principle by separating different management concerns.
Uses events data for comprehensive analytics.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_

from app.db.models.event import Event
from app.db.models.user import User
from app.db.models.book import Book
from app.db.models.loan import Loan
from app.db.models.order import BookOrder
from app.core.enums import OrderStatus
from app.schemas.statistics import LibraryOverview, BookStatistics, UserStatistics, OperationalStats


class LibraryStatisticsService:
    """
    Library management statistics service following Single Responsibility Principle.
    Provides actionable insights for library managers.
    """
    
    def __init__(self, db: Session):
        """Initialize with database session (Dependency Injection)."""
        self.db = db
    
    def get_library_overview(self) -> LibraryOverview:
        """
        Get overall library statistics for management dashboard.
        
        Returns:
            LibraryOverview: Key library metrics
        """
        total_books = sum(book.total_copies for book in self.db.query(Book))
        total_users = self.db.query(User).filter(User.is_active == True).count()
        total_loans = self.db.query(Loan).join(User).filter(User.is_active == True).count()
        
        books_on_loan = self.db.query(Loan).join(User).filter(
            User.is_active == True,
            Loan.return_date==None
        ).count()
        
        available_books = max(0, total_books - books_on_loan)
        
        today = datetime.datetime.now().date()
        overdue_loans = self.db.query(Loan).join(User).filter(
            User.is_active == True,
            and_(
                Loan.return_date == None,
                Loan.due_date < today
            )
        ).count()
        
        return LibraryOverview(
            total_books=total_books,
            total_users=total_users,
            total_loans=total_loans,
            available_books=available_books,
            books_on_loan=books_on_loan,
            overdue_loans=overdue_loans
        )
    
    def get_book_statistics(self) -> BookStatistics:
        """
        Get book-related statistics for inventory management.
        
        Returns:
            BookStatistics: Book management metrics
        """
        total_books = self.db.query(Book).count()
        
        books_on_loan = self.db.query(Loan).join(User).filter(
            User.is_active == True,
            Loan.return_date.is_(None)
        ).count()
        
        available_books = max(0, total_books - books_on_loan)
        
        genre_stats = self.db.query(
            Book.genre,
            func.count(Book.id)
        ).group_by(Book.genre).all()
        
        books_by_genre = {genre or "Unknown": count for genre, count in genre_stats}
        
        popular_books_query = self.db.query(
            Book.title,
            Book.author,
            func.count(Loan.id).label('loan_count')
        ).join(Loan).join(User).filter(User.is_active == True).group_by(Book.id, Book.title, Book.author).order_by(
            desc('loan_count')
        ).limit(10).all()
        
        most_borrowed_books = [
            {
                "title": title,
                "author": author,
                "loan_count": count
            } for title, author, count in popular_books_query
        ]
        
        return BookStatistics(
            total_books=total_books,
            books_by_genre=books_by_genre,
            most_borrowed_books=most_borrowed_books,
            available_books=available_books,
            books_on_loan=books_on_loan
        )
    
    def get_user_statistics(self) -> UserStatistics:
        """
        Get user-related statistics for patron management.
        
        Returns:
            UserStatistics: User management metrics
        """
        total_users = self.db.query(User).filter(User.is_active == True).count()
        
        active_users = self.db.query(User.id).join(Loan).filter(
            User.is_active == True,
            Loan.return_date.is_(None)
        ).distinct().count()
        
        month_start = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_users_this_month = self.db.query(User).filter(
            User.is_active == True,
            User.join_date >= month_start.date()
        ).count()
        
        top_borrowers_query = self.db.query(
            User.full_name,
            User.email,
            func.count(Loan.id).label('total_loans')
        ).join(Loan).filter(User.is_active == True).group_by(User.id, User.full_name, User.email).order_by(
            desc('total_loans')
        ).limit(10).all()
        
        top_borrowers = [
            {
                "full_name": full_name,
                "email": email,
                "total_loans": count
            } for full_name, email, count in top_borrowers_query
        ]
        
        today = datetime.datetime.now().date()
        users_with_overdue = self.db.query(User.id).join(Loan).filter(
            User.is_active == True,
            and_(
                Loan.return_date.is_(None),
                Loan.due_date < today
            )
        ).distinct().count()
        
        return UserStatistics(
            total_users=total_users,
            active_users=active_users,
            new_users_this_month=new_users_this_month,
            top_borrowers=top_borrowers,
            users_with_overdue=users_with_overdue
        )
    
    def get_operational_statistics(self) -> OperationalStats:
        """
        Get daily operational statistics for immediate management decisions.
        
        Returns:
            OperationalStats: Today's operational metrics
        """
        today = datetime.datetime.now().date()
        
        loans_today = self.db.query(Loan).join(User).filter(
            User.is_active == True,
            func.date(Loan.borrow_date) == today
        ).count()
        
        returns_today = self.db.query(Loan).join(User).filter(
            User.is_active == True,
            func.date(Loan.return_date) == today
        ).count()
        
        new_orders = self.db.query(BookOrder).join(User).filter(
            User.is_active == True,
            BookOrder.status == OrderStatus.WAITING
        ).count()
        
        last_24h = datetime.datetime.now() - timedelta(hours=24)
        system_events_today = self.db.query(Event).filter(
            Event.timestamp >= last_24h
        ).count()
        
        return OperationalStats(
            loans_today=loans_today,
            returns_today=returns_today,
            new_orders=new_orders,
            system_events_today=system_events_today,
        )


def get_statistics_service(db: Session) -> LibraryStatisticsService:
    """
    Factory function for creating statistics service.
    Follows Dependency Injection pattern used in your project.
    """
    return LibraryStatisticsService(db)
