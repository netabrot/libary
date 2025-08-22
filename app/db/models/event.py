from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, JSON, func
from sqlalchemy.orm import relationship

from app.db import Base

class Event(Base):
    """System log/event: what happened and when (optionally linked to a User)."""

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    event_type = Column(String, index=True)
    object_type = Column(String, index=True, nullable=True)
    duration_ms = Column(Integer, nullable=True)

    status_code = Column(Integer)
    method = Column(String)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True)
    user = relationship("User", back_populates="events")

    meta_data = Column(JSON, nullable=True)



    
