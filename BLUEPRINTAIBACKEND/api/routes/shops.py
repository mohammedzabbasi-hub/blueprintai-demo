from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from deps import get_current_active_user, get_db
from models.shop import Shop
from models.user import User
from schemas.shop import ShopConnectResponse, ShopOut

router = APIRouter()


@router.get("/", response_model=ShopOut)
def get_my_shop(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = db.query(Shop).filter(Shop.user_id == current_user.id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="No connected shop found")
    return shop


@router.post("/connect", response_model=ShopConnectResponse, status_code=status.HTTP_200_OK)
def connect_shop(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shop = db.query(Shop).filter(Shop.user_id == current_user.id).first()

    if not shop:
        shop = Shop(
            user_id=current_user.id,
            shop_name="My TikTok Shop",
            name="My TikTok Shop",
            tiktok_shop_id=f"shop_{current_user.id}",
            shop_code=f"shop_{current_user.id}",
        )
        db.add(shop)
        db.commit()
        db.refresh(shop)

    return ShopConnectResponse(
        message="Shop connected successfully",
        shop=shop,
        auth_url=None,
    )
