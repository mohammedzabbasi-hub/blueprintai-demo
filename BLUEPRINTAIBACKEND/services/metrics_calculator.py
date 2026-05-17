from typing import Any, Dict, List


def _get(obj: Any, key: str, default=0):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def safe_divide(numerator: float, denominator: float) -> float:
    try:
        if denominator in [0, None]:
            return 0.0
        return round(float(numerator) / float(denominator), 4)
    except Exception:
        return 0.0


def calculate_creative_metrics(creative: Any) -> Dict[str, Any]:
    views = float(_get(creative, "views", 0) or _get(creative, "total_views", 0) or 0)
    clicks = float(_get(creative, "clicks", 0) or 0)
    orders = float(_get(creative, "orders", 0) or _get(creative, "conversions", 0) or 0)
    revenue = float(_get(creative, "revenue", 0) or _get(creative, "total_revenue", 0) or 0)
    ad_spend = float(_get(creative, "ad_spend", 0) or _get(creative, "estimated_ad_spend", 0) or 0)
    likes = float(_get(creative, "likes", 0) or 0)
    shares = float(_get(creative, "shares", 0) or 0)
    comments = float(_get(creative, "comments", 0) or 0)

    ctr = safe_divide(clicks, views) * 100
    cvr = safe_divide(orders, clicks) * 100
    roas = safe_divide(revenue, ad_spend)
    engagement_rate = safe_divide(likes + comments + shares, views) * 100
    revenue_per_1k_views = safe_divide(revenue, views) * 1000

    return {
        "views": round(views),
        "clicks": round(clicks),
        "orders": round(orders),
        "revenue": round(revenue, 2),
        "ad_spend": round(ad_spend, 2),
        "likes": round(likes),
        "comments": round(comments),
        "shares": round(shares),
        "ctr": round(ctr, 2),
        "cvr": round(cvr, 2),
        "roas": round(roas, 2),
        "engagement_rate": round(engagement_rate, 2),
        "revenue_per_1k_views": round(revenue_per_1k_views, 2),
    }


def calculate_shop_totals(creatives: List[Any]) -> Dict[str, Any]:
    analyzed = [calculate_creative_metrics(c) for c in creatives]

    total_views = sum(c["views"] for c in analyzed)
    total_clicks = sum(c["clicks"] for c in analyzed)
    total_orders = sum(c["orders"] for c in analyzed)
    total_revenue = sum(c["revenue"] for c in analyzed)
    total_spend = sum(c["ad_spend"] for c in analyzed)

    return {
        "total_creatives": len(creatives),
        "total_views": total_views,
        "total_clicks": total_clicks,
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "total_ad_spend": round(total_spend, 2),
        "avg_ctr": round(safe_divide(total_clicks, total_views) * 100, 2),
        "avg_cvr": round(safe_divide(total_orders, total_clicks) * 100, 2),
        "avg_roas": round(safe_divide(total_revenue, total_spend), 2),
    }


def grade_metric(value: float, metric: str) -> str:
    if metric == "ctr":
        if value >= 3:
            return "Strong"
        if value >= 1.5:
            return "Average"
        return "Weak"

    if metric == "cvr":
        if value >= 5:
            return "Strong"
        if value >= 2:
            return "Average"
        return "Weak"

    if metric == "roas":
        if value >= 3:
            return "Profitable"
        if value >= 1.5:
            return "Borderline"
        return "Unprofitable"

    return "Unknown"


def classify_performance(metrics: Dict[str, Any]) -> str:
    ctr = metrics.get("ctr", 0)
    cvr = metrics.get("cvr", 0)
    roas = metrics.get("roas", 0)

    if roas >= 3 and ctr >= 2:
        return "Winning Creative"
    if ctr >= 2.5 and cvr < 2:
        return "High Interest, Low Conversion"
    if ctr < 1.5 and cvr >= 4:
        return "Weak Hook, Strong Buyer Intent"
    if metrics.get("ad_spend", 0) > 0 and roas < 1:
        return "Underperforming Creative"
    return "Average Creative"
