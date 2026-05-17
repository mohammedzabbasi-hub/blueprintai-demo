from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from deps import get_current_active_user, get_db
from models.shop import Shop
from models.user import User
from services.recommendation_service import get_recommendations

router = APIRouter()


@router.get("/")
def read_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = (
        db.query(Shop)
        .filter(Shop.user_id == current_user.id)
        .first()
    )

    if not shop:
        raise HTTPException(status_code=404, detail="No connected shop found")

    return get_recommendations(db=db, shop_id=shop.id)
