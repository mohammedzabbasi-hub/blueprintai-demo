from models.shop import Shop
from services.brief_service import generate_brief
from services.recommendation_service import get_recommendations
from services.tiktok_order_service import sync_orders
from services.tiktok_product_service import sync_products
from services.tiktok_service import sync_shop_creatives
from services.tiktok_shop_service import sync_shop_info


def run_full_shop_sync(db, shop_id: int) -> dict:
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise ValueError("Shop not found")

    synced_shop = sync_shop_info(db, getattr(shop, "connection", None)) if hasattr(shop, "connection") else shop
    products_count = sync_products(db, shop)
    orders_count = sync_orders(db, shop)
    creatives_count = sync_shop_creatives(db, shop)

    generated_briefs = 0
    seen_products = set()

    for creative in getattr(shop, "creatives", []):
        product_name = getattr(creative, "product", None)
        if product_name and product_name not in seen_products:
            generate_brief(db=db, shop_id=shop.id, product_name=product_name, brand_name=getattr(shop, "name", None))
            seen_products.add(product_name)
            generated_briefs += 1

    recommendations = get_recommendations(db=db, shop_id=shop.id)

    return {
        "shop_id": shop.id,
        "products_synced": products_count,
        "orders_synced": orders_count,
        "creatives_synced": creatives_count,
        "briefs_generated": generated_briefs,
        "recommendations_count": len(recommendations),
        "shop_refreshed": bool(synced_shop),
    }
