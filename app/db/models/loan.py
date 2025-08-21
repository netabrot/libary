from . import Base, Column, Integer, ForeignKey, Date,date,relativedelta, relationship

class Loan(Base):
    """A loan record: which User borrowed which book and when."""

    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False)
    borrow_date = Column(Date, nullable=False, default=date.today)
    due_date = Column(Date, nullable=False, default=date.today() + relativedelta(months=1))
    return_date = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")