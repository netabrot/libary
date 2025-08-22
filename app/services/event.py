from datetime import datetime, timezone
from typing import Any
from app.services.base import CRUDBase
from app.db.models.event import Event
from app.schemas.events import EventBase
from app.core.enums import EventType, ObjectType
from app.db.models.user import User

class CRUDEvent(CRUDBase[Event, EventBase, EventBase]):
    pass

event = CRUDEvent(Event)

def log_event(
    db,
    event_type: EventType,
    user: User | None = None,
    *,
    duration_ms: int | None = None,
    status_code: int | None = None,
    method: str | None = None,
    object_type: ObjectType | None = None,
    **meta: Any,
) -> Event:
    event_in = EventBase(
        event_type=event_type,
        object_type=object_type,
        duration_ms=duration_ms,
        status_code=status_code,
        method=method,
        user_id=(user.id if user else None),
        meta_data=(meta or None),
    )
    return event.create(db, obj_in=event_in)