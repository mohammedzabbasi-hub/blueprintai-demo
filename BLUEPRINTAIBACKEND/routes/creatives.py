from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from deps import get_current_active_user, get_db
from models.creative import Creative
from models.user import User
from schemas.creative import CreativeOut, CreativeSyncResponse
from services.tiktok_service import sync_shop_creatives
from services.shop_service import get_or_create_default_shop

router = APIRouter()


@router.post("/sync", response_model=CreativeSyncResponse, status_code=status.HTTP_200_OK)
def sync_creatives(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = get_or_create_default_shop(db, current_user)

    imported_count = sync_shop_creatives(db=db, shop=shop)

    return {
        "message": "Creatives synced successfully",
        "imported_count": imported_count,
    }


@router.get("/", response_model=list[CreativeOut])
def list_creatives(
    product: str | None = Query(default=None),
    creator_type: str | None = Query(default=None),
    hook_type: str | None = Query(default=None),
    ad_type: str | None = Query(default=None),
    humor_style: str | None = Query(default=None),
    delivery_style: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = get_or_create_default_shop(db, current_user)

    query = db.query(Creative).filter(Creative.shop_id == shop.id)

    if product:
        query = query.filter(Creative.product == product)

    if creator_type:
        query = query.filter(Creative.creator_type == creator_type)

    if hook_type:
        query = query.filter(Creative.hook_type == hook_type)

    if ad_type:
        query = query.filter(Creative.ad_type == ad_type)

    if humor_style:
        query = query.filter(Creative.humor_style == humor_style)

    if delivery_style:
        query = query.filter(Creative.delivery_style == delivery_style)

    if search:
        like_term = f"%{search}%"
        query = query.filter(
            or_(
                Creative.title.ilike(like_term),
                Creative.product.ilike(like_term),
                Creative.creator.ilike(like_term),
                Creative.transcript_summary.ilike(like_term),
                Creative.insight.ilike(like_term),
                Creative.ai_summary.ilike(like_term),
            )
        )

    creatives = query.order_by(Creative.id.desc()).all()

    return creatives


@router.get("/{creative_id}", response_model=CreativeOut)
def get_creative(
    creative_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = get_or_create_default_shop(db, current_user)

    creative = (
        db.query(Creative)
        .filter(
            Creative.id == creative_id,
            Creative.shop_id == shop.id,
        )
        .first()
    )

    if not creative:
        raise HTTPException(status_code=404, detail="Creative not found")

    return creative
