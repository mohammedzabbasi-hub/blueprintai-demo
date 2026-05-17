from collections import Counter

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from db.database import get_db
from models.shop import Shop
from models.creative import Creative
from models.metric import Metric

try:
    from models.brief import Brief
except Exception:
    Brief = None

try:
    from models.recommendation import Recommendation
except Exception:
    Recommendation = None


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
def read_dashboard_analytics(
    shop_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    shop_query = db.query(Shop)

    if shop_id is not None:
        shop = shop_query.filter(Shop.id == shop_id).first()
    else:
        shop = shop_query.first()

    if not shop:
        return {
            "shop": None,
            "totals": {
                "creatives": 0,
                "analyses": 0,
                "briefs": 0,
                "recommendations": 0,
                "views": 0,
                "orders": 0,
            },
            "patterns": {
                "hooks": {},
                "creator_types": {},
                "humor_styles": {},
                "delivery_styles": {},
            },
            "leaderboard": [],
        }

    creative_query = db.query(Creative).filter(Creative.shop_id == shop.id)
    creatives = creative_query.all()
    creative_ids = [creative.id for creative in creatives]

    total_views = sum(int(c.views or 0) for c in creatives)
    total_orders = sum(int(c.orders or 0) for c in creatives)

    analyses_count = 0

    briefs_count = 0
    if Brief is not None:
        try:
            briefs_count = db.query(Brief).filter(Brief.shop_id == shop.id).count()
        except Exception:
            briefs_count = 0

    recommendations_count = 0
    if Recommendation is not None:
        try:
            recommendations_count = (
                db.query(Recommendation)
                .filter(Recommendation.shop_id == shop.id)
                .count()
            )
        except Exception:
            recommendations_count = 0

    hooks = Counter(c.hook_type for c in creatives if c.hook_type)
    creator_types = Counter(c.creator_type for c in creatives if c.creator_type)
    humor_styles = Counter(c.humor_style for c in creatives if c.humor_style)
    delivery_styles = Counter(c.delivery_style for c in creatives if c.delivery_style)

    leaderboard = (
        creative_query
        .order_by(
            Creative.orders.desc(),
            Creative.views.desc(),
            Creative.score.desc(),
        )
        .limit(8)
        .all()
    )

    return {
        "shop": {
            "id": shop.id,
            "shop_name": shop.shop_name,
            "name": shop.name,
            "tiktok_shop_id": shop.tiktok_shop_id,
            "region": shop.region,
            "currency": shop.currency,
            "category": shop.shop_code,
        },
        "totals": {
            "creatives": len(creatives),
            "analyses": analyses_count,
            "briefs": briefs_count,
            "recommendations": recommendations_count,
            "views": total_views,
            "orders": total_orders,
        },
        "patterns": {
            "hooks": dict(hooks),
            "creator_types": dict(creator_types),
            "humor_styles": dict(humor_styles),
            "delivery_styles": dict(delivery_styles),
        },
        "leaderboard": [
            {
                "creative_id": creative.id,
                "id": creative.id,
                "title": creative.title,
                "product": creative.product,
                "creator": creative.creator,
                "creator_type": creative.creator_type,
                "hook_type": creative.hook_type,
                "engagement_score": creative.engagement_score,
                "conversion_score": creative.conversion_score,
                "score": creative.score,
                "views": creative.views,
                "likes": creative.likes,
                "shares": creative.shares,
                "clicks": creative.clicks,
                "orders": creative.orders,
            }
            for creative in leaderboard
        ],
    }
