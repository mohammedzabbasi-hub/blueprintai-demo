from typing import Any, Dict, List

from services.metrics_calculator import calculate_shop_totals
from services.pattern_engine import analyze_patterns, detect_shop_issues
from services.insight_scoring import build_insight, score_all_creatives


def _pattern_name(pattern):
    if not pattern:
        return "Unknown"
    return pattern.get("name", "Unknown")


def generate_recommendations(creatives: List[Any]) -> List[Dict[str, Any]]:
    if not creatives:
        return [{
            "title": "Add creatives to unlock recommendations",
            "finding": "No creative data was found for this shop.",
            "recommended_action": "Upload or sync TikTok Shop ad creatives so BluePrintAI can analyze patterns.",
            "priority": "High",
            "confidence": "Low",
            "sample_size": 0,
        }]

    totals = calculate_shop_totals(creatives)
    patterns = analyze_patterns(creatives)
    scored = score_all_creatives(creatives)
    issues = detect_shop_issues(creatives)

    recommendations = []

    best_hook = patterns.get("best_hook")
    worst_hook = patterns.get("worst_hook")
    best_creator = patterns.get("best_creator_type")
    best_style = patterns.get("best_visual_style")
    best_cta = patterns.get("best_cta")
    best_angle = patterns.get("best_product_angle")

    if best_hook:
        recommendations.append(build_insight(
            title=f"Create more ads using {_pattern_name(best_hook)} hooks",
            finding=f"{_pattern_name(best_hook)} hooks are currently your strongest hook pattern with {best_hook.get('roas')} ROAS and {best_hook.get('ctr')}% CTR.",
            action=f"Produce 3-5 new TikTok Shop creatives that open with a {_pattern_name(best_hook)} hook in the first 3 seconds.",
            sample_size=best_hook.get("count", 0),
            priority="High",
        ))

    if best_creator:
        recommendations.append(build_insight(
            title=f"Double down on {_pattern_name(best_creator)} creators",
            finding=f"{_pattern_name(best_creator)} creatives are producing the strongest creator-type performance.",
            action=f"Recruit or brief more {_pattern_name(best_creator)} creators for your next batch of TikTok Shop ads.",
            sample_size=best_creator.get("count", 0),
            priority="High",
        ))

    if best_style:
        recommendations.append(build_insight(
            title=f"Use more {_pattern_name(best_style)} creative formats",
            finding=f"{_pattern_name(best_style)} videos are currently outperforming other visual styles.",
            action=f"Turn your next product briefs into {_pattern_name(best_style)} style videos with a clear product demo and CTA.",
            sample_size=best_style.get("count", 0),
            priority="Medium",
        ))

    if best_cta:
        recommendations.append(build_insight(
            title=f"Repeat your best CTA style: {_pattern_name(best_cta)}",
            finding=f"{_pattern_name(best_cta)} CTAs are associated with stronger conversion performance.",
            action=f"Use this CTA style in your next 3 ad briefs and compare CVR against older CTA types.",
            sample_size=best_cta.get("count", 0),
            priority="Medium",
        ))

    if best_angle:
        recommendations.append(build_insight(
            title=f"Lean into the {_pattern_name(best_angle)} product angle",
            finding=f"The {_pattern_name(best_angle)} angle is connected to stronger revenue and ROAS.",
            action=f"Make new scripts that frame the product around {_pattern_name(best_angle).lower()} instead of broad lifestyle messaging.",
            sample_size=best_angle.get("count", 0),
            priority="Medium",
        ))

    if worst_hook and best_hook and worst_hook.get("name") != best_hook.get("name"):
        recommendations.append(build_insight(
            title=f"Reduce spend on {_pattern_name(worst_hook)} hooks",
            finding=f"{_pattern_name(worst_hook)} hooks are currently the weakest hook pattern.",
            action=f"Pause or rewrite creatives using {_pattern_name(worst_hook)} hooks unless they have a specific winning product or creator behind them.",
            sample_size=worst_hook.get("count", 0),
            priority="Medium",
        ))

    if totals.get("avg_ctr", 0) >= 2.5 and totals.get("avg_cvr", 0) < 2:
        recommendations.append(build_insight(
            title="Fix conversion after the click",
            finding="Your average CTR is strong, but average CVR is weak.",
            action="Improve the product page, pricing, offer, reviews, or landing experience because people are clicking but not buying.",
            sample_size=len(creatives),
            priority="High",
        ))

    if totals.get("avg_ctr", 0) < 1.5 and totals.get("avg_cvr", 0) >= 4:
        recommendations.append(build_insight(
            title="Improve the first 3 seconds of your ads",
            finding="Your CVR is strong, but CTR is weak.",
            action="Test stronger hooks, faster product reveals, and clearer pain points to attract more qualified clicks.",
            sample_size=len(creatives),
            priority="High",
        ))

    if issues:
        recommendations.append(build_insight(
            title="Review creatives with performance mismatches",
            finding=f"{len(issues)} creatives show mismatches like high clicks but low purchases or weak ROAS.",
            action="Open the Creative Library and revise the flagged creatives before scaling spend.",
            sample_size=len(issues),
            priority="Medium",
        ))

    if scored:
        top = scored[0]
        recommendations.append(build_insight(
            title=f"Turn your top ad into a repeatable template",
            finding=f"Your strongest creative is '{top.get('title')}' with a score of {top.get('score')}/100.",
            action="Create 3 variations of this ad using the same hook, structure, creator type, and CTA.",
            sample_size=1,
            priority="High",
        ))

    return recommendations[:8]


def generate_recommendation_report(creatives: List[Any]) -> Dict[str, Any]:
    return {
        "totals": calculate_shop_totals(creatives),
        "patterns": analyze_patterns(creatives),
        "issues": detect_shop_issues(creatives),
        "recommendations": generate_recommendations(creatives),
        "scored_creatives": score_all_creatives(creatives),
    }
