import json

from models.webhook_event import WebhookEvent


def record_webhook_event(db, topic: str, payload: dict):
    event = WebhookEvent()

    if hasattr(event, "topic"):
        event.topic = topic
    if hasattr(event, "event_type"):
        event.event_type = topic
    if hasattr(event, "payload"):
        event.payload = json.dumps(payload)
    if hasattr(event, "raw_payload"):
        event.raw_payload = json.dumps(payload)
    if hasattr(event, "status"):
        event.status = "received"

    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def should_trigger_resync(topic: str) -> bool:
    watched_topics = {
        "product.updated",
        "product.created",
        "order.status_updated",
        "order.created",
        "shop.updated",
        "content.updated",
    }
    return topic in watched_topics
