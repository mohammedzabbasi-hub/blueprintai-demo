from datetime import datetime
from pydantic import BaseModel


class WebhookReceiveResponse(BaseModel):
    message: str
    accepted: bool = True
    should_resync: bool = False


class WebhookEventOut(BaseModel):
    id: int
    source: str
    event_type: str | None = None
    signature: str | None = None
    payload: str
    is_processed: bool
    processed_at: datetime | None = None
    processing_error: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
