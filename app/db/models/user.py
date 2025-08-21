from . import Base, Column, Integer, String, Date, date, SAEnum, UserRole, Boolean, relationship

class User(Base):
    """Library User: a registered user who can borrow books."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    join_date = Column(Date, default=date.today)
    address = Column(String)
    password = Column(String)
    role = Column(SAEnum(UserRole), default=UserRole.MEMBER)
    is_active = Column(Boolean, default=False)

    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
