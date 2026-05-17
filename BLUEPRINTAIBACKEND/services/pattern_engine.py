from typing import Any, Dict, List
from collections import defaultdict

from services.metrics_calculator import calculate_creative_metrics, safe_divide
from services.creative_classifier import classify_creative


def _get(obj: Any, key: str, default=""):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def group_performance(creatives: List[Any], group_key: str) -> List[Dict[str, Any]]:
    groups = defaultdict(list)

    for creative in creatives:
        labels = classify_creative(creative)
        value = labels.get(group_key) or _get(creative, group_key, "Unknown")
        groups[value].append(creative)

    results = []

    for name, items in groups.items():
        metrics = [calculate_creative_metrics(c) for c in items]

        views = sum(m["views"] for m in metrics)
        clicks = sum(m["clicks"] for m in metrics)
        orders = sum(m["orders"] for m in metrics)
        revenue = sum(m["revenue"] for m in metrics)
        spend = sum(m["ad_spend"] for m in metrics)

        results.append({
            "name": name,
            "count": len(items),
            "views": views,
            "clicks": clicks,
            "orders": orders,
            "revenue": round(revenue, 2),
            "ad_spend": round(spend, 2),
            "ctr": round(safe_divide(clicks, views) * 100, 2),
            "cvr": round(safe_divide(orders, clicks) * 100, 2),
            "roas": round(safe_divide(revenue, spend), 2),
            "revenue_per_1k_views": round(safe_divide(revenue, views) * 1000, 2),
        })

    return sorted(results, key=lambda x: (x["roas"], x["revenue"], x["orders"]), reverse=True)


def find_best_and_worst(patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not patterns:
        return {"best": None, "worst": None}

    valid = [p for p in patterns if p["count"] >= 1]

    if not valid:
        return {"best": None, "worst": None}

    return {
        "best": valid[0],
        "worst": valid[-1],
    }


def analyze_patterns(creatives: List[Any]) -> Dict[str, Any]:
    hook_patterns = group_performance(creatives, "hook_type")
    creator_patterns = group_performance(creatives, "creator_type")
    visual_patterns = group_performance(creatives, "visual_style")
    cta_patterns = group_performance(creatives, "cta_type")
    angle_patterns = group_performance(creatives, "product_angle")

    return {
        "hook_patterns": hook_patterns,
        "creator_patterns": creator_patterns,
        "visual_style_patterns": visual_patterns,
        "cta_patterns": cta_patterns,
        "product_angle_patterns": angle_patterns,
        "best_hook": find_best_and_worst(hook_patterns)["best"],
        "worst_hook": find_best_and_worst(hook_patterns)["worst"],
        "best_creator_type": find_best_and_worst(creator_patterns)["best"],
        "worst_creator_type": find_best_and_worst(creator_patterns)["worst"],
        "best_visual_style": find_best_and_worst(visual_patterns)["best"],
        "worst_visual_style": find_best_and_worst(visual_patterns)["worst"],
        "best_cta": find_best_and_worst(cta_patterns)["best"],
        "best_product_angle": find_best_and_worst(angle_patterns)["best"],
    }


def detect_shop_issues(creatives: List[Any]) -> List[Dict[str, str]]:
    issues = []

    for creative in creatives:
        name = _get(creative, "title", "Untitled Creative")
        metrics = calculate_creative_metrics(creative)

        ctr = metrics["ctr"]
        cvr = metrics["cvr"]
        roas = metrics["roas"]

        if ctr >= 2.5 and cvr < 2:
            issues.append({
                "creative": name,
                "issue": "High CTR but low CVR",
                "meaning": "The ad gets attention and clicks, but the product page, offer, or audience targeting may not be converting.",
            })

        if ctr < 1.5 and cvr >= 4:
            issues.append({
                "creative": name,
                "issue": "Low CTR but strong CVR",
                "meaning": "The ad does not attract enough clicks, but people who click are likely to buy. Improve the hook.",
            })

        if metrics.get("ad_spend", 0) > 0 and roas < 1:
            issues.append({
                "creative": name,
                "issue": "Unprofitable ROAS",
                "meaning": "The creative is spending more than it earns and should be paused, revised, or tested with a new angle.",
            })

    return issues
