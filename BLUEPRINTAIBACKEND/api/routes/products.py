from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from deps import get_current_active_user, get_db
from models.product import Product
from models.shop import Shop
from models.user import User
from schemas.product import ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = db.query(Shop).filter(Shop.user_id == current_user.id).first()
    if not shop:
        return []
    return db.query(Product).filter(Product.shop_id == shop.id).order_by(Product.id.desc()).all()
