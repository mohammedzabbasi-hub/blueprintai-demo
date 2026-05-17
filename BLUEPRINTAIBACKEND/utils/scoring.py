def engagement_score(views: int = 0, likes: int = 0, comments: int = 0, shares: int = 0) -> float:
    if views <= 0:
        return 0.0
    return round(((likes * 1.0) + (comments * 1.5) + (shares * 2.0)) / views * 1000, 2)


def conversion_score(views: int = 0, clicks: int = 0, orders: int = 0) -> float:
    if views <= 0:
        return 0.0
    return round(((clicks * 1.5) + (orders * 4.0)) / views * 1000, 2)


def ctr(views: int = 0, clicks: int = 0) -> float:
    if views <= 0:
        return 0.0
    return round(clicks / views, 6)


def cvr(clicks: int = 0, orders: int = 0) -> float:
    if clicks <= 0:
        return 0.0
    return round(orders / clicks, 6)


def confidence_to_priority(confidence: int | None) -> str:
    confidence = confidence or 0
    if confidence >= 85:
        return "high"
    if confidence >= 65:
        return "medium"
    return "low"
