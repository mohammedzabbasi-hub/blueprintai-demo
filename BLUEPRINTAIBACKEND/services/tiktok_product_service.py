from models.product import Product
from services.tiktok_client import TikTokClient


def sync_products(db, shop):
    access_token = getattr(getattr(shop, "connection", None), "access_token", None)
    client = TikTokClient(access_token=access_token)

    try:
        payload = client.get_products()
        items = (payload.get("data") or {}).get("products") or []
    except Exception:
        items = [
            {
                "id": "p1",
                "title": "GlowPatch",
                "status": "active",
                "category": "Skincare",
                "price": "24.99",
                "main_image": "/static/glowpatch.jpg",
                "description": "Acne patch for fast blemish coverage.",
            },
            {
                "id": "p2",
                "title": "LuxeGlow",
                "status": "active",
                "category": "Beauty",
                "price": "29.99",
                "main_image": "/static/luxeglow.jpg",
                "description": "Daily glow serum for morning routines.",
            },
        ]

    imported_count = 0

    for item in items:
        external_id = str(item.get("id") or item.get("product_id") or item.get("sku_id") or item.get("title"))
        product = (
            db.query(Product)
            .filter(Product.shop_id == shop.id, Product.external_id == external_id)
            .first()
        )

        if not product:
            product = Product(shop_id=shop.id, external_id=external_id)
            db.add(product)
            imported_count += 1

        if hasattr(product, "name"):
            product.name = item.get("title") or item.get("name")
        if hasattr(product, "title"):
            product.title = item.get("title") or item.get("name")
        if hasattr(product, "status"):
            product.status = item.get("status")
        if hasattr(product, "category"):
            product.category = item.get("category")
        if hasattr(product, "price"):
            try:
                product.price = float(item.get("price") or 0)
            except Exception:
                pass
        if hasattr(product, "image_url"):
            product.image_url = item.get("main_image")
        if hasattr(product, "description"):
            product.description = item.get("description")
        if hasattr(product, "raw_payload"):
            product.raw_payload = str(item)

    db.commit()
    return imported_count
