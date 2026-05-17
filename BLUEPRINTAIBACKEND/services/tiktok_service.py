from models.creative import Creative
from models.metric import Metric
from services.creative_classifier import (
    classify_ad_type,
    classify_creator_type,
    classify_cta_style,
    classify_demo_style,
    classify_hook_type,
    classify_speaking_style,
)
from services.ai.ai_analysis_service import analyze_video_url


def sync_shop_creatives(db, shop):
    sample_creatives = [
        {
            "product": "GlowPatch",
            "title": "3-second acne fix demo",
            "creator": "Ava Lee",
            "thumbnail": "/static/glowpatch-1.jpg",
            "video_url": "https://www.tiktok.com/@example/video/1000000001",
            "insight": "Strong early hook and fast product payoff.",
            "score": 91,
            "views": 1200000,
            "likes": 54000,
            "shares": 3200,
            "clicks": 18000,
            "orders": 2400,
            "date": "2024-03-10",
        },
        {
            "product": "LuxeGlow",
            "title": "Morning routine tutorial",
            "creator": "Mia Chen",
            "thumbnail": "/static/luxeglow-1.jpg",
            "video_url": "https://www.tiktok.com/@example/video/1000000002",
            "insight": "Tutorial-style content performs well for this product.",
            "score": 86,
            "views": 860000,
            "likes": 41000,
            "shares": 2100,
            "clicks": 12400,
            "orders": 1700,
            "date": "2024-03-14",
        },
    ]

    imported_count = 0

    for item in sample_creatives:
        existing = (
            db.query(Creative)
            .filter(Creative.shop_id == shop.id, Creative.title == item["title"])
            .first()
        )

        creator_type = classify_creator_type(item["creator"], item["title"])
        ad_type = classify_ad_type(item["title"])
        hook_type = classify_hook_type(item["title"])
        speaking_style = classify_speaking_style(item["title"])
        demo_style = classify_demo_style(item["title"])
        cta_style = classify_cta_style(item["title"])

        ai_result = analyze_video_url(
            db=db,
            shop_id=shop.id,
            video_url=item.get("video_url", ""),
            brand_name=getattr(shop, "name", None),
            product_name=item["product"],
        )

        signals = ai_result.signals if ai_result else None

        creative_payload = {
            **item,
            "creator_type": creator_type,
            "creator_archetype": getattr(signals, "creator_style", None) or creator_type,
            "ad_type": ad_type,
            "hook_type": getattr(signals, "hook_type", None) or hook_type,
            "hook_text": getattr(signals, "hook_text", None),
            "speaking_style": speaking_style,
            "demo_style": demo_style,
            "cta_style": getattr(signals, "cta_style", None) or cta_style,
            "humor_style": getattr(signals, "humor_style", None),
            "delivery_style": getattr(signals, "delivery_style", None),
            "primary_subject": getattr(signals, "subject_focus", None),
            "pacing": getattr(signals, "pacing", None),
            "transcript": ai_result.transcript if ai_result else None,
            "transcript_summary": ai_result.transcript_summary if ai_result else None,
            "ai_summary": item.get("insight"),
            "winning_reason": ai_result.performance_hypothesis if ai_result else item.get("insight"),
        }

        if existing:
            for key, value in creative_payload.items():
                setattr(existing, key, value)
            creative = existing
        else:
            creative = Creative(shop_id=shop.id, **creative_payload)
            db.add(creative)
            db.flush()
            imported_count += 1

        ctr = (creative_payload["clicks"] / creative_payload["views"]) if creative_payload["views"] else 0
        cvr = (creative_payload["orders"] / creative_payload["clicks"]) if creative_payload["clicks"] else 0

        metric = db.query(Metric).filter(Metric.creative_id == creative.id).first()

        if metric:
            metric.views = creative_payload["views"]
            metric.clicks = creative_payload["clicks"]
            metric.likes = creative_payload["likes"]
            metric.shares = creative_payload["shares"]
            metric.orders = creative_payload["orders"]
            metric.ctr = ctr
            metric.cvr = cvr
            metric.roas = None
        else:
            db.add(
                Metric(
                    creative_id=creative.id,
                    views=creative_payload["views"],
                    clicks=creative_payload["clicks"],
                    likes=creative_payload["likes"],
                    shares=creative_payload["shares"],
                    orders=creative_payload["orders"],
                    ctr=ctr,
                    cvr=cvr,
                    roas=None,
                )
            )

    db.commit()
    return imported_count
