from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from services.recommendation_service import build_recommendations_for_shop

router = APIRouter(tags=["recommendations"])


@router.get("/recommendations")
def get_recommendations(
    shop_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return build_recommendations_for_shop(db=db, shop_id=shop_id)
