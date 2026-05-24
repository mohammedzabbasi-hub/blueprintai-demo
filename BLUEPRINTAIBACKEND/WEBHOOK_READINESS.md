# TikTok Webhook Readiness

This document captures the Phase 11 webhook readiness review. It is
documentation only. Do not mount webhook routes, delete duplicate files, or
change route behavior until validation and idempotency are implemented and
tested.

## Current Status

No TikTok webhook route is currently mounted in `main.py`.

That means `POST /webhooks/tiktok` is not currently active, even though multiple
webhook route files exist in the repository.

## Duplicate Webhook Files

The repo currently contains three webhook route files:

| File | Route declared | Mounted today? | Notes |
|---|---|---:|---|
| `routes/webhooks.py` | `POST /webhooks/tiktok` | no | Imports missing `store_and_process_webhook` |
| `api/routes/webhooks.py` | `POST /webhooks/tiktok` | no | Uses existing `record_webhook_event` and `should_trigger_resync` |
| `routes/webhooks copy.py` | `POST /webhooks/tiktok` | no | Duplicate copy of `routes/webhooks.py`; imports missing `store_and_process_webhook` |

## Recommended Future Keeper

Prefer `api/routes/webhooks.py` as the future webhook route implementation.

Reasons:

- It imports service functions that exist today.
- It has a simpler event-recording path.
- It is easier to upgrade safely with signature validation and idempotency.

## Risky Files

`routes/webhooks.py` and `routes/webhooks copy.py` are risky because both import:

```python
store_and_process_webhook
```

That function is not defined in `services/tiktok_webhook_service.py` today.
Mounting either route file as-is would likely cause an import/startup failure.

`routes/webhooks copy.py` is also a duplicate copy file and should not become the
source of truth.

## Missing TikTok Signature Validation

Webhook signature validation is not production-ready.

Current gaps:

- `api/routes/webhooks.py` does not read or validate TikTok signature headers.
- `routes/webhooks.py` accepts `x_tts_signature`, but delegates to a missing
  service function.
- `config.py` does not define a webhook secret or official signing config.
- The official TikTok signing headers and canonical payload rules still need to
  be confirmed before implementation.

Do not invent signature validation rules. Confirm the official TikTok Shop
webhook signing requirements first.

## Missing Idempotency Protection

Webhook idempotency is not production-ready.

Current gaps:

- Repeated webhook deliveries can create duplicate event rows.
- No official external event ID is extracted from the payload.
- No uniqueness constraint prevents duplicate processing.
- There is no safe "already received" response path.
- Processing status is present in the model, but not enough to prevent duplicate
  processing by itself.

TikTok and other webhook providers commonly retry deliveries. The backend needs
to treat duplicate delivery as expected behavior.

## Existing `webhook_events` Model

The repo already has a `WebhookEvent` model in `models/webhook_event.py`.

Current fields include:

- `id`
- `source`
- `event_type`
- `signature`
- `payload`
- `is_processed`
- `processed_at`
- `processing_error`
- `created_at`

This is a useful starting point for durable webhook storage.

## Recommended Future Schema Addition

Add an external event identifier once the official TikTok payload shape is
confirmed:

- `external_event_id` or `event_id`

Add a uniqueness constraint to prevent duplicate delivery processing:

- unique on `source + external_event_id`

The exact field name should match the official TikTok event identifier if one is
provided.

## Safe Future Implementation Plan

For a later implementation phase:

1. Confirm official TikTok Shop webhook signing headers and validation rules.
2. Choose one route file to keep, preferably `api/routes/webhooks.py`.
3. Add config for the official webhook signing secret or equivalent validation
   setting.
4. Verify the raw request body, not re-serialized JSON.
5. Reject missing or invalid signatures with an appropriate 4xx response.
6. Parse payload only after signature validation passes.
7. Extract official event type/topic and external event ID.
8. Store raw payload, signature/header metadata, event type, and external event
   ID.
9. Add uniqueness protection on `source + external_event_id`.
10. Handle duplicate deliveries safely by returning success without duplicate
    processing.
11. Track processing status with `is_processed`, `processed_at`, and
    `processing_error`.
12. Add tests for missing signature, invalid signature, valid signature,
    duplicate delivery, malformed JSON, and unknown event type.
13. Mount only one webhook router in `main.py` after tests pass.
14. Deprecate duplicate webhook route files in a separate cleanup phase.

## Warning

Do not mount webhook routes until signature validation and idempotency are
implemented.

Mounting an unvalidated webhook endpoint can expose the backend to spoofed
events, duplicate processing, noisy retries, and TikTok Shop App Store review
failure.
