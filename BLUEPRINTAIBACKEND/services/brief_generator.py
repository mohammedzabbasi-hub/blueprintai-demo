from typing import Any, Dict, List

from services.pattern_engine import analyze_patterns
from services.recommendation_engine import generate_recommendations


def _get(obj: Any, key: str, default=""):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def generate_brief_from_pattern(
    product_name: str,
    hook_type: str,
    creator_type: str,
    visual_style: str,
    product_angle: str,
    cta_type: str,
) -> Dict[str, Any]:
    hook_templates = {
        "Problem/Solution": f"Still dealing with this problem? This {product_name} fixes it fast.",
        "Curiosity/Shock": f"I did not expect this {product_name} to work this well.",
        "Before/After": f"Here is the before and after from using this {product_name}.",
        "Review/Testimonial": f"I tested this {product_name} so you do not have to.",
        "Tutorial": f"Here is how to use this {product_name} in under 20 seconds.",
        "Offer/Discount": f"This {product_name} is on deal right now, and here is why it is worth it.",
    }

    hook = hook_templates.get(hook_type, f"Here is why people are buying this {product_name}.")

    return {
        "product_name": product_name,
        "brief_title": f"{hook_type} {visual_style} Ad for {product_name}",
        "creator_type": creator_type,
        "hook_type": hook_type,
        "visual_style": visual_style,
        "product_angle": product_angle,
        "cta_type": cta_type,
        "script": [
            {
                "scene": 1,
                "goal": "Hook attention immediately",
                "direction": hook,
            },
            {
                "scene": 2,
                "goal": "Show the product clearly",
                "direction": f"Show the {product_name} close-up and make the main benefit obvious.",
            },
            {
                "scene": 3,
                "goal": "Prove the product works",
                "direction": f"Demonstrate the {product_angle.lower()} benefit with a real use case.",
            },
            {
                "scene": 4,
                "goal": "Push the viewer to act",
                "direction": f"End with a {cta_type} CTA and tell viewers to buy through TikTok Shop.",
            },
        ],
        "editing_notes": [
            "Show the product within the first 3 seconds.",
            "Use captions for every major claim.",
            "Keep the video fast, clear, and product-focused.",
            "Avoid long intros.",
        ],
    }


def generate_briefs_for_shop(creatives: List[Any], product_name: str = None) -> List[Dict[str, Any]]:
    if not product_name:
        product_name = "your product"

    patterns = analyze_patterns(creatives) if creatives else {}

    best_hook = patterns.get("best_hook", {}) or {}
    best_creator = patterns.get("best_creator_type", {}) or {}
    best_style = patterns.get("best_visual_style", {}) or {}
    best_cta = patterns.get("best_cta", {}) or {}
    best_angle = patterns.get("best_product_angle", {}) or {}

    hook = best_hook.get("name", "Problem/Solution")
    creator = best_creator.get("name", "UGC Creator")
    style = best_style.get("name", "Product Demo")
    cta = best_cta.get("name", "Shop Now")
    angle = best_angle.get("name", "Pain Point")

    return [
        generate_brief_from_pattern(product_name, hook, creator, style, angle, cta),
        generate_brief_from_pattern(product_name, "Review/Testimonial", creator, "Talking Head", angle, "Get Yours"),
        generate_brief_from_pattern(product_name, "Problem/Solution", "UGC Creator", "Product Demo", "Convenience", "Shop Now"),
    ]


def generate_brief_report(creatives: List[Any], product_name: str = None) -> Dict[str, Any]:
    return {
        "product_name": product_name or "your product",
        "strategy_basis": generate_recommendations(creatives),
        "briefs": generate_briefs_for_shop(creatives, product_name),
    }
