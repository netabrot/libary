from fastapi.encoders import jsonable_encoder

from app.db.models.event import Event
from app.schemas.events import EventBase
from app.services.base import CRUDBase


class CRUDEvent(CRUDBase[Event, EventBase, EventBase]):
    pass


crud_event = CRUDEvent(Event)


def log_event(db, *, user=None, duration_ms=None, status_code=None, method=None, object_type=None, **meta) -> Event:
    event_in = EventBase(
        duration_ms=duration_ms,
        status_code=status_code,
        method=method,
        user_id=(user.id if user else None),
        meta_data=jsonable_encoder(meta) if meta is not None else None
    )
    return crud_event.create(db, obj_in=event_in)
