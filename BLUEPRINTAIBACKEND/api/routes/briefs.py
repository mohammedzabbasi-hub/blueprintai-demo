from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from deps import get_db
from models.creative import Creative
from models.shop import Shop
from schemas.briefs import BriefGenerateRequest, BriefOut
from services.brief_generator import generate_briefs_for_shop
from services.brief_service import generate_brief

router = APIRouter()


@router.get("")
def get_ad_briefs(
    shop_id: int = Query(...),
    product_name: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        return {"shop_id": shop_id, "briefs": []}

    creatives = db.query(Creative).filter(Creative.shop_id == shop_id).all()

    return {
        "shop_id": shop.id,
        "shop_name": shop.shop_name or shop.name or f"Shop {shop.id}",
        "briefs": generate_briefs_for_shop(creatives, product_name),
    }


@router.post("/generate", response_model=BriefOut, status_code=status.HTTP_200_OK)
def generate_ad_brief(
    brief_in: BriefGenerateRequest,
    db: Session = Depends(get_db),
):
    brief = generate_brief(
        db=db,
        shop_id=1,
        product_name=brief_in.product_name,
        brand_name=brief_in.brand_name,
    )

    return brief
