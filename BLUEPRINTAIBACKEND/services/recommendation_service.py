from collections import defaultdict

from models.shop import Shop
from models.creative import Creative
from models.metric import Metric


def num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def pct(value):
    return round(value * 100, 2)


def safe_rate(top, bottom):
    bottom = num(bottom)
    if bottom <= 0:
        return 0
    return num(top) / bottom


def avg(values):
    values = [num(v) for v in values if v is not None]
    if not values:
        return 0
    return sum(values) / len(values)


def group_by_field(creatives, field):
    groups = defaultdict(list)

    for creative in creatives:
        value = getattr(creative, field, None)

        if value:
            groups[str(value)].append(creative)

    return groups


def summarize_group(items):
    views = sum(num(c.views) for c in items)
    clicks = sum(num(c.clicks) for c in items)
    orders = sum(num(c.orders) for c in items)
    likes = sum(num(c.likes) for c in items)
    comments = sum(num(getattr(c, "comments", 0)) for c in items)
    shares = sum(num(c.shares) for c in items)
    revenue = sum(num(getattr(c, "revenue", 0)) for c in items)

    return {
        "count": len(items),
        "views": views,
        "clicks": clicks,
        "orders": orders,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "revenue": revenue,
        "ctr": safe_rate(clicks, views),
        "conversion_rate": safe_rate(orders, clicks),
        "engagement_rate": safe_rate(likes + comments + shares, views),
        "avg_score": avg([getattr(c, "score", 0) for c in items]),
    }


def best_group(creatives, field, metric="conversion_rate", minimum_count=1):
    groups = group_by_field(creatives, field)
    ranked = []

    for name, items in groups.items():
        if len(items) < minimum_count:
            continue

        stats = summarize_group(items)
        ranked.append((name, stats))

    if not ranked:
        return None

    ranked.sort(key=lambda item: item[1].get(metric, 0), reverse=True)
    return ranked[0]


def worst_group(creatives, field, metric="conversion_rate", minimum_count=1):
    groups = group_by_field(creatives, field)
    ranked = []

    for name, items in groups.items():
        if len(items) < minimum_count:
            continue

        stats = summarize_group(items)
        ranked.append((name, stats))

    if not ranked:
        return None

    ranked.sort(key=lambda item: item[1].get(metric, 0))
    return ranked[0]


def creative_name(creative):
    return getattr(creative, "title", None) or getattr(creative, "caption", None) or "Untitled Creative"


def build_recommendations_for_shop(db, shop_id=None):
    shop_query = db.query(Shop)

    if shop_id is not None:
        shop = shop_query.filter(Shop.id == shop_id).first()
    else:
        shop = shop_query.first()

    if not shop:
        return {
            "shop": None,
            "summary": {
                "creative_score": 0,
                "top_priority": "Connect a shop",
                "best_opportunity": "No shop data available",
                "expected_lift": "0%",
            },
            "recommendations": [],
        }

    creatives = (
        db.query(Creative)
        .filter(Creative.shop_id == shop.id)
        .all()
    )

    creative_ids = [creative.id for creative in creatives]
    if creative_ids:
        metric_rows = db.query(Metric).filter(Metric.creative_id.in_(creative_ids)).all()
        metric_totals = {}
        for metric in metric_rows:
            bucket = metric_totals.setdefault(
                metric.creative_id,
                {"views": 0, "clicks": 0, "orders": 0, "likes": 0, "shares": 0},
            )
            for field in bucket:
                bucket[field] += int(getattr(metric, field, 0) or 0)

        for creative in creatives:
            totals = metric_totals.get(creative.id, {})
            for field, value in totals.items():
                if value and not num(getattr(creative, field, 0)):
                    setattr(creative, field, value)

    if not creatives:
        return {
            "shop": {
                "id": shop.id,
                "name": shop.shop_name or shop.name or "Connected Shop",
                "category": getattr(shop, "shop_code", None) or "TikTok Shop",
            },
            "summary": {
                "creative_score": 0,
                "top_priority": "Add creative data",
                "best_opportunity": "Analyze or seed creatives first",
                "expected_lift": "0%",
            },
            "recommendations": [],
        }

    total_views = sum(num(c.views) for c in creatives)
    total_clicks = sum(num(c.clicks) for c in creatives)
    total_orders = sum(num(c.orders) for c in creatives)
    total_likes = sum(num(c.likes) for c in creatives)
    total_comments = sum(num(getattr(c, "comments", 0)) for c in creatives)
    total_shares = sum(num(c.shares) for c in creatives)

    overall_ctr = safe_rate(total_clicks, total_views)
    overall_conversion = safe_rate(total_orders, total_clicks)
    overall_engagement = safe_rate(total_likes + total_comments + total_shares, total_views)
    avg_score = round(avg([getattr(c, "score", 0) for c in creatives]))

    recommendations = []

    best_hook = best_group(creatives, "hook_type", "conversion_rate")
    weak_hook = worst_group(creatives, "hook_type", "conversion_rate")

    if best_hook:
        hook_name, stats = best_hook
        recommendations.append({
            "id": "best-hook",
            "category": "Hooks",
            "name": f"Make more creatives using {hook_name} hooks",
            "rec_type": "Scale Winner",
            "priority": "High",
            "confidence": min(95, 65 + stats["count"] * 5),
            "product_name": "All products",
            "reason": f"{hook_name} is currently the strongest hook pattern for this shop.",
            "action": f"Create 3-5 new videos that open with a {hook_name} hook in the first 3 seconds.",
            "evidence": f"{stats['count']} creatives using this hook generated {int(stats['orders'])} orders with a {pct(stats['conversion_rate'])}% click-to-order conversion rate.",
        })

    if weak_hook and best_hook and weak_hook[0] != best_hook[0]:
        hook_name, stats = weak_hook
        recommendations.append({
            "id": "weak-hook",
            "category": "Hooks",
            "name": f"Reduce or rewrite {hook_name} hooks",
            "rec_type": "Fix Weakness",
            "priority": "Medium",
            "confidence": min(90, 60 + stats["count"] * 5),
            "product_name": "All products",
            "reason": f"{hook_name} is underperforming compared with stronger hook formats.",
            "action": f"Rewrite these videos with a clearer problem, faster product reveal, or stronger first line.",
            "evidence": f"{stats['count']} creatives using this hook have a {pct(stats['conversion_rate'])}% click-to-order conversion rate.",
        })

    best_ad_style = best_group(creatives, "ad_type", "conversion_rate") or best_group(creatives, "ad_style", "conversion_rate")

    if best_ad_style:
        style_name, stats = best_ad_style
        recommendations.append({
            "id": "best-ad-style",
            "category": "Creative Format",
            "name": f"Scale {style_name} style videos",
            "rec_type": "Creative Format",
            "priority": "High",
            "confidence": min(94, 65 + stats["count"] * 5),
            "product_name": "All products",
            "reason": f"{style_name} creatives are converting better than other formats.",
            "action": f"Use {style_name} as the main format for the next batch of TikTok Shop videos.",
            "evidence": f"{stats['count']} {style_name} creatives produced {int(stats['orders'])} orders and {int(stats['clicks'])} clicks.",
        })

    best_creator_type = best_group(creatives, "creator_type", "conversion_rate")

    if best_creator_type:
        creator_type, stats = best_creator_type
        recommendations.append({
            "id": "best-creator-type",
            "category": "Creator Strategy",
            "name": f"Prioritize {creator_type} creators",
            "rec_type": "Creator Strategy",
            "priority": "High",
            "confidence": min(92, 65 + stats["count"] * 5),
            "product_name": "All products",
            "reason": f"{creator_type} creatives are producing stronger shop performance.",
            "action": f"Recruit or assign more {creator_type} creators for the next testing cycle.",
            "evidence": f"{creator_type} creatives generated {int(stats['orders'])} orders with a {pct(stats['conversion_rate'])}% conversion rate.",
        })

    best_creator = best_group(creatives, "creator", "conversion_rate")

    if best_creator:
        creator, stats = best_creator
        recommendations.append({
            "id": "best-creator",
            "category": "Creator Strategy",
            "name": f"Give {creator} more product tests",
            "rec_type": "Scale Creator",
            "priority": "Medium",
            "confidence": min(90, 60 + stats["count"] * 5),
            "product_name": "All products",
            "reason": f"{creator} is one of the strongest creators for this shop.",
            "action": f"Have {creator} test another product angle, bundle, or offer this week.",
            "evidence": f"{creator} has {int(stats['orders'])} attributed orders across {stats['count']} creatives.",
        })

    high_view_low_order = sorted(
        [
            c for c in creatives
            if num(c.views) >= max(1000, total_views / max(len(creatives), 1))
            and safe_rate(num(c.orders), num(c.clicks)) < overall_conversion
        ],
        key=lambda c: num(c.views),
        reverse=True,
    )

    if high_view_low_order:
        creative = high_view_low_order[0]
        recommendations.append({
            "id": "high-view-low-order",
            "category": "Conversion",
            "name": "Fix high-view videos that are not converting",
            "rec_type": "Conversion Fix",
            "priority": "High",
            "confidence": 86,
            "product_name": getattr(creative, "product", None) or "Unknown product",
            "reason": "Some videos are getting attention but are not turning enough viewers into buyers.",
            "action": "Add stronger product proof, price framing, and a clearer TikTok Shop call-to-action.",
            "evidence": f"'{creative_name(creative)}' has {int(num(creative.views))} views but only {int(num(creative.orders))} orders.",
        })

    low_ctr_creatives = sorted(
        [
            c for c in creatives
            if num(c.views) > 0 and safe_rate(num(c.clicks), num(c.views)) < overall_ctr
        ],
        key=lambda c: safe_rate(num(c.clicks), num(c.views))
    )

    if low_ctr_creatives:
        creative = low_ctr_creatives[0]
        recommendations.append({
            "id": "low-ctr",
            "category": "CTA",
            "name": "Improve click-through with clearer CTAs",
            "rec_type": "CTA Fix",
            "priority": "Medium",
            "confidence": 82,
            "product_name": getattr(creative, "product", None) or "Unknown product",
            "reason": "The shop has creatives where viewers watch but do not click enough.",
            "action": "Use direct CTA language like 'Tap the product card' or 'Shop the bundle before the deal ends.'",
            "evidence": f"'{creative_name(creative)}' has a {pct(safe_rate(num(creative.clicks), num(creative.views)))}% CTR, below the shop average of {pct(overall_ctr)}%.",
        })

    product_winner = best_group(creatives, "product", "conversion_rate")

    if product_winner:
        product, stats = product_winner
        recommendations.append({
            "id": "best-product",
            "category": "Product Positioning",
            "name": f"Build more content around {product}",
            "rec_type": "Product Focus",
            "priority": "Medium",
            "confidence": min(88, 60 + stats["count"] * 5),
            "product_name": product,
            "reason": f"{product} is currently one of the strongest products in the creative data.",
            "action": f"Create new angles for {product}: problem-solution, comparison, testimonial, and quick demo.",
            "evidence": f"{product} creatives generated {int(stats['orders'])} orders with a {pct(stats['conversion_rate'])}% conversion rate.",
        })

    if overall_engagement < 0.05:
        recommendations.append({
            "id": "low-engagement",
            "category": "Engagement",
            "name": "Make videos feel more native to TikTok",
            "rec_type": "Engagement Fix",
            "priority": "Medium",
            "confidence": 78,
            "product_name": "All products",
            "reason": "Engagement is below a healthy benchmark for short-form creative testing.",
            "action": "Use more creator reactions, casual filming, text overlays, and comment-style hooks.",
            "evidence": f"The shop engagement rate is {pct(overall_engagement)}%.",
        })

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recommendations.sort(key=lambda item: priority_order.get(item["priority"], 3))

    return {
        "shop": {
            "id": shop.id,
            "name": shop.shop_name or shop.name or "Connected Shop",
            "category": getattr(shop, "shop_code", None) or "TikTok Shop",
        },
        "summary": {
            "creative_score": avg_score,
            "top_priority": recommendations[0]["name"] if recommendations else "No recommendation yet",
            "best_opportunity": best_hook[0] if best_hook else "Collect more creative data",
            "expected_lift": "+10-20%",
            "total_creatives": len(creatives),
            "total_views": int(total_views),
            "total_clicks": int(total_clicks),
            "total_orders": int(total_orders),
            "ctr": pct(overall_ctr),
            "conversion_rate": pct(overall_conversion),
            "engagement_rate": pct(overall_engagement),
        },
        "recommendations": recommendations[:10],
    }
