from app.db.models.models import Event, User
from app.schemas.events import EventBase

def log_event(db, event_type: str, user: User | None = None, **meta):
    event_in = EventBase(event_type=event_type,
                         user_id=user.id if user else None, meta_data={**meta, **({"email": user.email} if user else {})})
    return create_event(db, obj_in=event_in)

def create_event(db, *, obj_in: EventBase) -> Event:
    data = obj_in.model_dump() 
    db_obj = Event(**data)
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except:
        db.rollback()
        raise