from . import Base, Column, Integer,DateTime,func,JSON,ForeignKey, String, relationship

class Event(Base):
    """System log/event: what happened and when (optionally linked to a User)."""

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    event_type = Column(String, index=True)
    meta_data = Column(JSON, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True)
    user = relationship("User", back_populates="events")
