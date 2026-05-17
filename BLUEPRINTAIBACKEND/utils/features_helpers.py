from collections import Counter

from utils.scoring import conversion_score, engagement_score


def summarize_creative_patterns(creatives) -> dict:
    hook_counter = Counter()
    creator_counter = Counter()
    humor_counter = Counter()
    delivery_counter = Counter()

    for creative in creatives:
        if getattr(creative, "hook_type", None):
            hook_counter[creative.hook_type] += 1
        if getattr(creative, "creator_type", None):
            creator_counter[creative.creator_type] += 1
        if getattr(creative, "humor_style", None):
            humor_counter[creative.humor_style] += 1
        if getattr(creative, "delivery_style", None):
            delivery_counter[creative.delivery_style] += 1

    return {
        "hooks": dict(hook_counter),
        "creator_types": dict(creator_counter),
        "humor_styles": dict(humor_counter),
        "delivery_styles": dict(delivery_counter),
    }


def build_creative_scorecard(creative) -> dict:
    return {
        "creative_id": creative.id,
        "title": creative.title,
        "product": creative.product,
        "hook_type": getattr(creative, "hook_type", None),
        "creator_type": getattr(creative, "creator_type", None),
        "engagement_score": engagement_score(
            views=getattr(creative, "views", 0) or 0,
            likes=getattr(creative, "likes", 0) or 0,
            comments=getattr(creative, "comments", 0) or 0,
            shares=getattr(creative, "shares", 0) or 0,
        ),
        "conversion_score": conversion_score(
            views=getattr(creative, "views", 0) or 0,
            clicks=getattr(creative, "clicks", 0) or 0,
            orders=getattr(creative, "orders", 0) or 0,
        ),
    }
    
