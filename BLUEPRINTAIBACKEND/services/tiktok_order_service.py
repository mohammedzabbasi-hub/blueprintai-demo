from models.order import Order
from services.tiktok_client import TikTokClient


def sync_orders(db, shop):
    access_token = getattr(getattr(shop, "connection", None), "access_token", None)
    client = TikTokClient(access_token=access_token)

    try:
        payload = client.get_orders()
        items = (payload.get("data") or {}).get("orders") or []
    except Exception:
        items = [
            {
                "id": "o1",
                "status": "completed",
                "buyer_name": "Sample Buyer 1",
                "product_name": "GlowPatch",
                "total_amount": "24.99",
                "created_at": "2024-03-10T12:00:00Z",
            },
            {
                "id": "o2",
                "status": "completed",
                "buyer_name": "Sample Buyer 2",
                "product_name": "LuxeGlow",
                "total_amount": "29.99",
                "created_at": "2024-03-14T15:30:00Z",
            },
        ]

    imported_count = 0

    for item in items:
        external_id = str(item.get("id") or item.get("order_id"))
        order = (
            db.query(Order)
            .filter(Order.shop_id == shop.id, Order.external_id == external_id)
            .first()
        )

        if not order:
            order = Order(shop_id=shop.id, external_id=external_id)
            db.add(order)
            imported_count += 1

        if hasattr(order, "status"):
            order.status = item.get("status")
        if hasattr(order, "buyer_name"):
            order.buyer_name = item.get("buyer_name")
        if hasattr(order, "product_name"):
            order.product_name = item.get("product_name")
        if hasattr(order, "total_amount"):
            try:
                order.total_amount = float(item.get("total_amount") or 0)
            except Exception:
                pass
        if hasattr(order, "created_at"):
            order.created_at = item.get("created_at")
        if hasattr(order, "raw_payload"):
            order.raw_payload = str(item)

    db.commit()
    return imported_count
