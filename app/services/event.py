from datetime import datetime, timezone
from typing import Any

from fastapi.encoders import jsonable_encoder
from app.services.base import CRUDBase
from app.db.models.event import Event
from app.schemas.events import EventBase
from app.db.models.user import User

class CRUDEvent(CRUDBase[Event, EventBase, EventBase]):
    pass

crud_event = CRUDEvent(Event)
def log_event(db, event_type, *, user=None,duration_ms=None, status_code=None, method=None, object_type=None, **meta) -> Event:
    event_in = EventBase(
        event_type=event_type,
        object_type=object_type,
        duration_ms=duration_ms,
        status_code=status_code,
        method=method,
        user_id=(user.id if user else None),
        meta_data=jsonable_encoder(meta) if meta is not None else None
    )
    return crud_event.create(db, obj_in=event_in)