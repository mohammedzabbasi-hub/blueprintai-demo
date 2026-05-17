from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from db.database import get_db
from services.tiktok_webhook_service import store_and_process_webhook

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/tiktok")
async def tiktok_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_tts_signature: str | None = Header(default=None),
):
    payload = await request.json()
    try:
        result = store_and_process_webhook(
            db=db,
            payload=payload,
            signature=x_tts_signature,
        )
        return {"success": True, "event_id": result["event_id"], "processed": result["processed"]}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
