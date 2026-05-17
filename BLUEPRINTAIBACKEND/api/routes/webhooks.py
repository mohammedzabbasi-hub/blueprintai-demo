from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from fastapi import Depends

from deps import get_db
from schemas.webhook import WebhookReceiveResponse
from services.tiktok_webhook_service import record_webhook_event, should_trigger_resync

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/tiktok", response_model=WebhookReceiveResponse)
async def receive_tiktok_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await request.json()
    topic = payload.get("type") or payload.get("topic") or "unknown"
    record_webhook_event(db=db, topic=topic, payload=payload)
    return WebhookReceiveResponse(
        message="Webhook received",
        accepted=True,
        should_resync=should_trigger_resync(topic),
    )
