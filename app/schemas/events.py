from . import BaseModel, datetime, Field, timezone, Any, ConfigDict

class EventBase(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str
    meta_data: dict[str, Any] | None = None
    user_id: int | None = None

class ShowEvent(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)