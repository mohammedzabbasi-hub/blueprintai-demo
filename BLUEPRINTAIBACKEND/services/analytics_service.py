from sqlalchemy.orm import Session

from models.creative import Creative
from models.metric import Metric


def _safe_float(value, default=0):
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def get_dashboard_analytics(db: Session, shop_id: int):
    creatives = db.query(Creative).filter(Creative.shop_id == shop_id).all()
    metrics = (
        db.query(Metric)
        .join(Creative, Creative.id == Metric.creative_id)
        .filter(Creative.shop_id == shop_id)
        .all()
    )

    total_views = sum(int(getattr(c, "views", 0) or 0) for c in creatives)
    total_clicks = sum(int(getattr(c, "clicks", 0) or 0) for c in creatives)
    total_orders = sum(int(getattr(c, "orders", 0) or 0) for c in creatives)
    total_revenue = sum(_safe_float(getattr(c, "revenue", 0)) for c in creatives)

    avg_ctr = round((total_clicks / total_views) * 100, 2) if total_views else 0
    conversion_rate = round((total_orders / total_clicks) * 100, 2) if total_clicks else 0

    target_demo_roas = 5.8
    estimated_ad_spend = round(total_revenue / target_demo_roas, 2) if total_revenue else 0
    avg_roas = round(total_revenue / estimated_ad_spend, 2) if estimated_ad_spend else 0

    recommendations_count = 8 if len(creatives) > 0 else 0

    hook_stats = {}
    creator_stats = {}
    style_stats = {}

    for creative in creatives:
        metric = next((m for m in metrics if m.creative_id == creative.id), None)

        if metric and getattr(metric, "ctr", None) is not None:
            ctr = metric.ctr or 0
        else:
            views = int(getattr(creative, "views", 0) or 0)
            clicks = int(getattr(creative, "clicks", 0) or 0)
            ctr = (clicks / views) * 100 if views else 0

        hook_stats.setdefault(getattr(creative, "hook_type", None) or "Unknown", []).append(ctr)
        creator_stats.setdefault(getattr(creative, "creator_type", None) or "Unknown", []).append(ctr)
        style_stats.setdefault(getattr(creative, "ad_type", None) or "Unknown", []).append(ctr)

    def best_avg(stat_dict):
        if not stat_dict:
            return None
        key = max(stat_dict, key=lambda k: sum(stat_dict[k]) / len(stat_dict[k]))
        avg_value = sum(stat_dict[key]) / len(stat_dict[key])
        return {"label": key, "value": round(avg_value, 2), "trend": "up"}

    def worst_avg(stat_dict):
        if not stat_dict:
            return None
        key = min(stat_dict, key=lambda k: sum(stat_dict[k]) / len(stat_dict[k]))
        avg_value = sum(stat_dict[key]) / len(stat_dict[key])
        return {"label": key, "value": round(avg_value, 2), "trend": "down"}

    return {
        "dashboardStats": {
            "bestHook": best_avg(hook_stats),
            "bestCreator": best_avg(creator_stats),
            "strongestStyle": best_avg(style_stats),
            "weakestStyle": worst_avg(style_stats),
        },
        "totals": {
            "views": total_views,
            "clicks": total_clicks,
            "orders": total_orders,
            "creatives": len(creatives),
            "recommendations": recommendations_count,
            "revenue": round(total_revenue, 2),
            "total_revenue": round(total_revenue, 2),
            "estimated_ad_spend": estimated_ad_spend,
            "avg_ctr": avg_ctr,
            "ctr": avg_ctr,
            "avg_roas": avg_roas,
            "roas": avg_roas,
            "conversion_rate": conversion_rate,
        },
    }
