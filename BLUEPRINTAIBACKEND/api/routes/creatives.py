from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from deps import get_current_active_user
from db.database import get_db
from models.creative import Creative
from models.shop import Shop
from models.user import User
from routes.login import DEMO_ACCOUNTS
from routes.personalized import verify_shop_access


router = APIRouter(tags=["creatives"])


def creative_to_dict(creative: Creative):
    return {
        "id": creative.id,
        "shop_id": creative.shop_id,
        "product_id": creative.product_id,
        "product": creative.product,
        "title": creative.title,
        "creator": creative.creator,
        "source_platform": creative.source_platform,
        "video_url": creative.video_url,
        "thumbnail": creative.thumbnail,
        "insight": creative.insight,
        "transcript": creative.transcript,
        "transcript_summary": creative.transcript_summary,
        "creator_type": creative.creator_type,
        "creator_archetype": creative.creator_archetype,
        "promoter_handle": creative.promoter_handle,
        "humor_style": creative.humor_style,
        "delivery_style": creative.delivery_style,
        "speaking_style": creative.speaking_style,
        "demo_style": creative.demo_style,
        "ad_type": creative.ad_type,
        "hook_type": creative.hook_type,
        "hook_text": creative.hook_text,
        "cta_style": creative.cta_style,
        "primary_subject": creative.primary_subject,
        "visual_style": creative.visual_style,
        "pacing": creative.pacing,
        "text_overlay_style": creative.text_overlay_style,
        "winning_reason": creative.winning_reason,
        "ai_summary": creative.ai_summary,
        "score": creative.score,
        "engagement_score": creative.engagement_score,
        "conversion_score": creative.conversion_score,
        "views": creative.views,
        "likes": creative.likes,
        "comments": creative.comments,
        "shares": creative.shares,
        "clicks": creative.clicks,
        "orders": creative.orders,
        "date": creative.date,
    }


@router.get("/")
def get_creatives(
    shop_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if shop_id is None:
        email = str(getattr(current_user, "email", "") or "").lower()
        if email in DEMO_ACCOUNTS:
            raise HTTPException(status_code=400, detail="shop_id is required for demo accounts")

        shop = db.query(Shop).filter(Shop.user_id == current_user.id).first()
        if not shop:
            return []
        shop_id = shop.id
    else:
        verify_shop_access(db.connection(), shop_id, current_user)

    query = db.query(Creative)

    query = query.filter(Creative.shop_id == shop_id)

    creatives = query.order_by(Creative.orders.desc(), Creative.views.desc()).all()

    return [creative_to_dict(creative) for creative in creatives]


@router.get("/{creative_id}")
def get_creative(
    creative_id: int,
    shop_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    verify_shop_access(db.connection(), shop_id, current_user)

    creative = (
        db.query(Creative)
        .filter(Creative.id == creative_id, Creative.shop_id == shop_id)
        .first()
    )

    if not creative:
        raise HTTPException(status_code=404, detail="Creative not found")

    return creative_to_dict(creative)
