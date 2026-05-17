def estimate_engagement_score(views: int, likes: int, shares: int, comments: int) -> float:
    if views <= 0:
        return 0.0
    return round(((likes * 1.0) + (shares * 2.0) + (comments * 1.5)) / views * 1000, 2)


def estimate_conversion_score(clicks: int, orders: int, views: int) -> float:
    if views <= 0:
        return 0.0
    return round(((clicks * 1.5) + (orders * 4.0)) / views * 1000, 2)


def choose_priority(confidence: int) -> str:
    if confidence >= 85:
        return "high"
    if confidence >= 65:
        return "medium"
    return "low"
