from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from deps import get_current_active_user, get_db
from models.creative import Creative
from models.shop import Shop
from models.user import User
from schemas.ai_analysis import (
    CompareVideosRequest,
    ComparisonInsightOut,
    VideoAnalysisOut,
    VideoIngestRequest,
)
from services.ai.ai_analysis_service import analyze_video_url, compare_creatives_for_shop

router = APIRouter(prefix="/tiktok", tags=["tiktok-intelligence"])


@router.post("/analyze", response_model=VideoAnalysisOut)
def analyze_tiktok_video(
    payload: VideoIngestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = db.query(Shop).filter(Shop.user_id == current_user.id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="No connected shop found")
    if not payload.url:
        raise HTTPException(status_code=400, detail="A video URL is required")

    return analyze_video_url(
        db=db,
        shop_id=shop.id,
        video_url=str(payload.url),
        brand_name=payload.brand_name,
        product_name=payload.product_name,
    )


@router.post("/compare", response_model=ComparisonInsightOut)
def compare_tiktok_creatives(
    payload: CompareVideosRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = db.query(Shop).filter(Shop.user_id == current_user.id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="No connected shop found")

    creatives = (
        db.query(Creative)
        .filter(Creative.shop_id == shop.id, Creative.id.in_(payload.creative_ids))
        .all()
    )

    if not creatives:
        raise HTTPException(status_code=404, detail="No creatives found for comparison")

    return compare_creatives_for_shop(creatives)
