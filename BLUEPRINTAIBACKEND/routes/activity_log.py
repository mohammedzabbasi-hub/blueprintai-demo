from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import json

from db.database import get_db
from models.activity_log import ActivityLog

router = APIRouter(prefix="/activity-log", tags=["activity-log"])

class ActivityLogCreate(BaseModel):
    user_email: str
    user_name: Optional[str] = None
    shop_id: Optional[int] = None
    activity_type: str
    title: str
    description: Optional[str] = None
    metadata: Optional[dict] = None

@router.post("/")
def create_activity_log(payload: ActivityLogCreate, db: Session = Depends(get_db)):
    item = ActivityLog(
        user_email=payload.user_email.lower().strip(),
        user_name=payload.user_name,
        shop_id=payload.shop_id,
        activity_type=payload.activity_type,
        title=payload.title,
        description=payload.description,
        metadata_json=json.dumps(payload.metadata or {}),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "user_email": item.user_email,
        "user_name": item.user_name,
        "shop_id": item.shop_id,
        "activity_type": item.activity_type,
        "title": item.title,
        "description": item.description,
        "created_at": item.created_at,
    }

@router.get("/")
def get_activity_logs(
    user_email: str = Query(...),
    shop_id: Optional[int] = Query(None),
    activity_type: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(ActivityLog).filter(ActivityLog.user_email == user_email.lower().strip())

    if shop_id is not None:
        query = query.filter(ActivityLog.shop_id == shop_id)

    if activity_type and activity_type != "all":
        query = query.filter(ActivityLog.activity_type == activity_type)

    items = query.order_by(ActivityLog.created_at.desc()).limit(limit).all()

    return [
        {
            "id": item.id,
            "user_email": item.user_email,
            "user_name": item.user_name,
            "shop_id": item.shop_id,
            "activity_type": item.activity_type,
            "title": item.title,
            "description": item.description,
            "created_at": item.created_at,
        }
        for item in items
    ]

@router.delete("/")
def clear_activity_logs(
    user_email: str = Query(...),
    shop_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(ActivityLog).filter(ActivityLog.user_email == user_email.lower().strip())

    if shop_id is not None:
        query = query.filter(ActivityLog.shop_id == shop_id)

    deleted = query.delete()
    db.commit()
    return {"deleted": deleted}
