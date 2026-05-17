from models.shop import Shop
from services.tiktok_client import TikTokClient


def sync_shop_info(db, shop_connection):
    client = TikTokClient(access_token=shop_connection.access_token)
    payload = client.get_shop_info()

    shop_data = (payload.get("data") or {}).get("shops") or []
    if not shop_data:
        return None

    remote_shop = shop_data[0]

    shop = (
        db.query(Shop)
        .filter(Shop.connection_id == shop_connection.id)
        .first()
    )

    if not shop:
        shop = Shop(connection_id=shop_connection.id)
        db.add(shop)

    if hasattr(shop, "name"):
        shop.name = remote_shop.get("shop_name") or remote_shop.get("name")
    if hasattr(shop, "shop_code"):
        shop.shop_code = remote_shop.get("shop_id") or remote_shop.get("cipher")
    if hasattr(shop, "region"):
        shop.region = remote_shop.get("region")
    if hasattr(shop, "currency"):
        shop.currency = remote_shop.get("currency")
    if hasattr(shop, "raw_payload"):
        shop.raw_payload = str(remote_shop)

    db.commit()
    db.refresh(shop)
    return shop
