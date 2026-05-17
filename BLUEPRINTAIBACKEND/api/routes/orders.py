from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from deps import get_current_active_user, get_db
from models.order import Order
from models.shop import Shop
from models.user import User
from schemas.order import OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = db.query(Shop).filter(Shop.user_id == current_user.id).first()
    if not shop:
        return []
    return db.query(Order).filter(Order.shop_id == shop.id).order_by(Order.id.desc()).all()
