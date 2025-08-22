from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict

from app.core.enums import EventType, ObjectType

class EventBase(BaseModel):
    event_type: EventType
    object_type: ObjectType | None = None
    status_code: int | None = None
    method: str | None = None
    user_id: int | None = None
    meta_data: dict[str, Any] | None = None
    duration_ms: int | None = None
    model_config = ConfigDict(extra="ignore")

class ShowEvent(EventBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
