import json
from pathlib import Path

from db.database import SessionLocal, engine
from db.base import Base

from models.shop import Shop
from models.creator import Creator
from models.creative import Creative
from models.metric import Metric

# Import these so SQLAlchemy knows about related models if they exist
try:
    from models.product import Product
except Exception:
    Product = None

try:
    from models.video_analysis import VideoAnalysis
except Exception:
    VideoAnalysis = None


DEMO_DIR = Path("demo_data/shops")


def safe_int(value, default=0):
    try:
        return int(value or default)
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        return float(value or default)
    except Exception:
        return default


def seed_demo_shops():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        files = sorted(DEMO_DIR.glob("*.json"))

        if not files:
            print("No demo JSON files found in demo_data/shops")
            return

        print(f"Found {len(files)} demo shop files")

        # Clear old demo data
        demo_shops = db.query(Shop).filter(Shop.tiktok_shop_id.like("demo_shop_%")).all()
        demo_shop_ids = [shop.id for shop in demo_shops]

        if demo_shop_ids:
            demo_creatives = db.query(Creative).filter(Creative.shop_id.in_(demo_shop_ids)).all()
            demo_creative_ids = [creative.id for creative in demo_creatives]

            if demo_creative_ids:
                db.query(Metric).filter(Metric.creative_id.in_(demo_creative_ids)).delete(synchronize_session=False)

            db.query(Creative).filter(Creative.shop_id.in_(demo_shop_ids)).delete(synchronize_session=False)
            db.query(Creator).filter(Creator.brand_id.in_(demo_shop_ids)).delete(synchronize_session=False)
            db.query(Shop).filter(Shop.id.in_(demo_shop_ids)).delete(synchronize_session=False)

            db.commit()
            print("Cleared old demo shop data")

        for file_path in files:
            print(f"Importing {file_path.name}")

            with open(file_path, "r") as f:
                data = json.load(f)

            shop_data = data.get("shop", {})
            summary = data.get("summary", {})
            creators = data.get("creators", [])
            creatives = data.get("creatives", [])

            shop = Shop(
                user_id=None,
                connection_id=shop_data.get("shop_id"),
                shop_name=shop_data.get("shop_name"),
                name=shop_data.get("shop_name"),
                tiktok_shop_id=shop_data.get("shop_id"),
                shop_code=shop_data.get("category"),
                region=shop_data.get("region"),
                currency=shop_data.get("currency"),
                raw_payload=json.dumps({
                    "metadata": data.get("metadata", {}),
                    "summary": summary,
                    "shop": shop_data
                }),
            )

            db.add(shop)
            db.commit()
            db.refresh(shop)

            creator_lookup = {}

            for creator_data in creators:
                creator = Creator(
                    user_id=None,
                    brand_id=shop.id,
                    name=creator_data.get("creator_name") or "Unknown Creator",
                    tiktok_handle=creator_data.get("tiktok_handle") or "@unknown",
                    profile_image=creator_data.get("profile_image"),
                    follower_count=safe_int(creator_data.get("follower_count")),
                    category=creator_data.get("collaboration_type"),
                    notes=json.dumps(creator_data),
                    total_videos=safe_int(creator_data.get("total_videos")),
                    total_views=safe_int(creator_data.get("total_views")),
                    total_likes=safe_int(creator_data.get("total_likes")),
                    total_comments=safe_int(creator_data.get("total_comments")),
                    total_shares=safe_int(creator_data.get("total_shares")),
                    total_conversions=safe_int(creator_data.get("total_orders")),
                    total_revenue=safe_int(creator_data.get("total_revenue")),
                )

                db.add(creator)
                db.flush()

                creator_lookup[creator_data.get("creator_id")] = creator

            db.commit()

            products_by_id = {
                product.get("product_id"): product
                for product in data.get("products", [])
            }

            for creative_data in creatives:
                creator_obj = creator_lookup.get(creative_data.get("creator_id"))
                product_obj = products_by_id.get(creative_data.get("product_id"), {})

                views = safe_int(creative_data.get("views"))
                likes = safe_int(creative_data.get("likes"))
                comments = safe_int(creative_data.get("comments"))
                shares = safe_int(creative_data.get("shares"))
                clicks = safe_int(creative_data.get("clicks"))
                orders = safe_int(creative_data.get("orders"))

                engagement_score = 0
                if views > 0:
                    engagement_score = round(((likes + comments + shares) / views) * 100, 2)

                conversion_score = safe_float(creative_data.get("conversion_rate"))

                creative = Creative(
                    shop_id=shop.id,
                    product_id=None,

                    product=product_obj.get("product_name") or "Unknown Product",
                    title=creative_data.get("caption") or "Untitled Creative",
                    creator=creator_obj.name if creator_obj else "Unknown Creator",

                    source_platform="tiktok",
                    video_url=creative_data.get("video_url"),
                    thumbnail=creative_data.get("thumbnail_url"),
                    insight=f"{creative_data.get('hook_type', 'Unknown hook')} creative for {product_obj.get('product_name', 'product')}",
                    transcript="",
                    transcript_summary=creative_data.get("caption"),

                    creator_type=creator_obj.category if creator_obj else None,
                    promoter_handle=creator_obj.tiktok_handle if creator_obj else None,
                    ad_type=creative_data.get("ad_style"),
                    hook_type=creative_data.get("hook_type"),
                    visual_style=creative_data.get("visual_style"),
                    hook_text=creative_data.get("caption"),
                    ai_summary=f"Demo creative with {views:,} views, {orders:,} orders, and ${safe_float(creative_data.get('revenue')):,.2f} revenue.",
                    raw_ai_json=json.dumps(creative_data),

                    score=round((engagement_score + conversion_score) / 2),
                    engagement_score=engagement_score,
                    conversion_score=conversion_score,

                    views=views,
                    likes=likes,
                    comments=comments,
                    shares=shares,
                    clicks=clicks,
                    orders=orders,

                    date=creative_data.get("posted_date"),
                )

                db.add(creative)
                db.flush()

                metric = Metric(
                    creative_id=creative.id,
                    views=views,
                    clicks=clicks,
                    likes=likes,
                    shares=shares,
                    orders=orders,
                    ctr=round((clicks / views) * 100, 2) if views else 0,
                    cvr=round((orders / clicks) * 100, 2) if clicks else 0,
                    roas=None,
                )

                db.add(metric)

            db.commit()

            print(
                f"Imported shop: {shop.shop_name} | "
                f"{len(creators)} creators | {len(creatives)} creatives"
            )

        print("Demo shop seed complete")

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_shops()
