from sqlalchemy.orm import Session

from models.creative import Creative
from models.metric import Metric


def get_dashboard_analytics(db: Session, shop_id: int):
    creatives = db.query(Creative).filter(Creative.shop_id == shop_id).all()
    metrics = (
        db.query(Metric)
        .join(Creative, Creative.id == Metric.creative_id)
        .filter(Creative.shop_id == shop_id)
        .all()
    )

    total_views = sum(m.views or 0 for m in metrics)
    total_clicks = sum(m.clicks or 0 for m in metrics)
    total_orders = sum(m.orders or 0 for m in metrics)

    hook_stats = {}
    creator_stats = {}
    style_stats = {}

    for creative in creatives:
        metric = next((m for m in metrics if m.creative_id == creative.id), None)
        if not metric:
            continue

        ctr = metric.ctr or 0
        hook_stats.setdefault(creative.hook_type, []).append(ctr)
        creator_stats.setdefault(creative.creator_type, []).append(ctr)
        style_stats.setdefault(creative.ad_type, []).append(ctr)

    def best_avg(stat_dict):
        if not stat_dict:
            return None
        key = max(stat_dict, key=lambda k: sum(stat_dict[k]) / len(stat_dict[k]))
        avg_value = sum(stat_dict[key]) / len(stat_dict[key])
        return {"label": key, "value": round(avg_value, 4), "trend": "up"}

    def worst_avg(stat_dict):
        if not stat_dict:
            return None
        key = min(stat_dict, key=lambda k: sum(stat_dict[k]) / len(stat_dict[k]))
        avg_value = sum(stat_dict[key]) / len(stat_dict[key])
        return {"label": key, "value": round(avg_value, 4), "trend": "down"}

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
        },
    }
