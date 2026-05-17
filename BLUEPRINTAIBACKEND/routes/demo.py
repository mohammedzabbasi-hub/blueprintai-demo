from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.shop import Shop
from models.creative import Creative
from models.creator import Creator


router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/shops")
def get_demo_shops(db: Session = Depends(get_db)):
    shops = (
        db.query(Shop)
        .filter(Shop.tiktok_shop_id.like("demo_shop_%"))
        .order_by(Shop.id.asc())
        .all()
    )

    results = []

    for shop in shops:
        creative_count = db.query(Creative).filter(Creative.shop_id == shop.id).count()
        creator_count = db.query(Creator).filter(Creator.brand_id == shop.id).count()

        results.append({
            "id": shop.id,
            "shop_name": shop.shop_name,
            "name": shop.name,
            "tiktok_shop_id": shop.tiktok_shop_id,
            "region": shop.region,
            "currency": shop.currency,
            "category": shop.shop_code,
            "creative_count": creative_count,
            "creator_count": creator_count,
        })

    return results
