from typing import Any, Dict, List

from services.metrics_calculator import calculate_creative_metrics, classify_performance
from services.creative_classifier import classify_creative


def score_creative(metrics: Dict[str, Any]) -> int:
    score = 0

    ctr = metrics.get("ctr", 0)
    cvr = metrics.get("cvr", 0)
    roas = metrics.get("roas", 0)
    engagement = metrics.get("engagement_rate", 0)

    if ctr >= 3:
        score += 25
    elif ctr >= 1.5:
        score += 15
    else:
        score += 5

    if cvr >= 5:
        score += 25
    elif cvr >= 2:
        score += 15
    else:
        score += 5

    if roas >= 3:
        score += 35
    elif roas >= 1.5:
        score += 20
    else:
        score += 5

    if engagement >= 5:
        score += 15
    elif engagement >= 2:
        score += 10
    else:
        score += 3

    return min(score, 100)


def confidence_from_sample_size(count: int) -> str:
    if count >= 20:
        return "High"
    if count >= 8:
        return "Medium"
    return "Low"


def score_single_creative(creative: Any) -> Dict[str, Any]:
    metrics = calculate_creative_metrics(creative)
    labels = classify_creative(creative)
    score = score_creative(metrics)

    return {
        "labels": labels,
        "metrics": metrics,
        "score": score,
        "performance_status": classify_performance(metrics),
    }


def score_all_creatives(creatives: List[Any]) -> List[Dict[str, Any]]:
    scored = []

    for creative in creatives:
        item = score_single_creative(creative)

        if isinstance(creative, dict):
            title = creative.get("title", "Untitled Creative")
            creative_id = creative.get("id")
        else:
            title = getattr(creative, "title", "Untitled Creative")
            creative_id = getattr(creative, "id", None)

        item["creative_id"] = creative_id
        item["title"] = title
        scored.append(item)

    return sorted(scored, key=lambda x: x["score"], reverse=True)


def build_insight(title: str, finding: str, action: str, sample_size: int, priority: str = "Medium") -> Dict[str, Any]:
    return {
        "title": title,
        "finding": finding,
        "recommended_action": action,
        "priority": priority,
        "confidence": confidence_from_sample_size(sample_size),
        "sample_size": sample_size,
    }
