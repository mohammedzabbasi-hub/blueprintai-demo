from typing import Any, Dict, List

from services.metrics_calculator import calculate_shop_totals
from services.pattern_engine import analyze_patterns, detect_shop_issues
from services.recommendation_engine import generate_recommendations
from services.brief_generator import generate_briefs_for_shop


def write_dashboard_summary(creatives: List[Any]) -> str:
    if not creatives:
        return "No creative data is available yet. Connect a shop, sync demo data, or upload creatives to unlock strategy insights."

    totals = calculate_shop_totals(creatives)
    patterns = analyze_patterns(creatives)

    best_hook = patterns.get("best_hook") or {}
    best_creator = patterns.get("best_creator_type") or {}
    best_style = patterns.get("best_visual_style") or {}

    return (
        f"Your shop has {totals['total_creatives']} tracked creatives with an average CTR of "
        f"{totals['avg_ctr']}%, CVR of {totals['avg_cvr']}%, and ROAS of {totals['avg_roas']}. "
        f"The strongest pattern right now is {best_hook.get('name', 'unknown')} hooks, especially when paired "
        f"with {best_creator.get('name', 'UGC Creator')} creators and {best_style.get('name', 'Product Demo')} videos."
    )


def write_strategy_summary(creatives: List[Any]) -> Dict[str, Any]:
    totals = calculate_shop_totals(creatives)
    patterns = analyze_patterns(creatives)
    issues = detect_shop_issues(creatives)
    recommendations = generate_recommendations(creatives)

    return {
        "dashboard_summary": write_dashboard_summary(creatives),
        "main_strength": _main_strength(patterns),
        "main_weakness": _main_weakness(totals, issues),
        "next_move": recommendations[0]["recommended_action"] if recommendations else "Add more creative data.",
        "recommendations": recommendations,
        "totals": totals,
        "patterns": patterns,
        "issues": issues,
    }


def _main_strength(patterns: Dict[str, Any]) -> str:
    best_hook = patterns.get("best_hook") or {}
    best_creator = patterns.get("best_creator_type") or {}

    if best_hook and best_creator:
        return f"{best_hook.get('name')} hooks with {best_creator.get('name')} creators are your strongest current creative direction."

    return "Your strongest pattern is not clear yet because more creative data is needed."


def _main_weakness(totals: Dict[str, Any], issues: List[Dict[str, Any]]) -> str:
    if totals.get("avg_ctr", 0) >= 2.5 and totals.get("avg_cvr", 0) < 2:
        return "Your ads are getting clicks, but the conversion path after the click needs improvement."

    if totals.get("avg_ctr", 0) < 1.5:
        return "Your main weakness is weak scroll-stopping power in the first few seconds."

    if totals.get("total_ad_spend", 0) > 0 and totals.get("avg_roas", 0) < 1.5:
        return "Your main weakness is profitability. Some creatives may need to be paused or rewritten."

    if issues:
        return "Some creatives have performance mismatches that should be reviewed."

    return "No major weakness is obvious yet."


def build_ai_prompt_payload(creatives: List[Any], product_name: str = None) -> Dict[str, Any]:
    """
    This function prepares clean structured data that you can later send to Gemini/OpenAI.
    For now, it does not call an external AI API.
    """
    return {
        "role": "TikTok Shop creative strategist",
        "instruction": "Use this structured data only. Do not invent metrics.",
        "strategy_summary": write_strategy_summary(creatives),
        "briefs": generate_briefs_for_shop(creatives, product_name),
    }
