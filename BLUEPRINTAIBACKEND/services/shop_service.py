from sqlalchemy.orm import Session

from models.shop import Shop
from models.user import User


def get_or_create_default_shop(db: Session, user: User) -> Shop:
    shop = db.query(Shop).filter(Shop.user_id == user.id).first()

    if shop:
        return shop

    shop = Shop(
        user_id=user.id,
        connection_id=None,
        shop_name="Default Workspace",
        name="Default Workspace",
        tiktok_shop_id=None,
        shop_code=None,
        region="US",
        currency="USD",
        raw_payload=None,
    )

    db.add(shop)
    db.commit()
    db.refresh(shop)

    return shop
