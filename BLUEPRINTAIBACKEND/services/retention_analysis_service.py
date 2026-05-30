import json
from bisect import bisect_left
from typing import Any


STRONG_DEMO_CURVE = [
    {"second": 0, "retention": 100},
    {"second": 3, "retention": 91},
    {"second": 5, "retention": 84},
    {"second": 10, "retention": 76},
    {"second": 15, "retention": 68},
    {"second": 20, "retention": 61},
    {"second": 30, "retention": 52},
]

AVERAGE_DEMO_CURVE = [
    {"second": 0, "retention": 100},
    {"second": 3, "retention": 82},
    {"second": 5, "retention": 69},
    {"second": 10, "retention": 53},
    {"second": 15, "retention": 44},
    {"second": 20, "retention": 37},
    {"second": 30, "retention": 29},
]

WEAK_DEMO_CURVE = [
    {"second": 0, "retention": 100},
    {"second": 3, "retention": 78},
    {"second": 5, "retention": 61},
    {"second": 10, "retention": 39},
    {"second": 15, "retention": 31},
    {"second": 20, "retention": 24},
    {"second": 30, "retention": 18},
]


def parse_retention_payload(retention_data: str | None) -> list[dict[str, float]] | None:
    if not retention_data:
        return None

    try:
        payload = json.loads(retention_data)
    except json.JSONDecodeError:
        return None

    curve = payload.get("retention_curve") if isinstance(payload, dict) else payload
    if not isinstance(curve, list):
        return None

    return normalize_retention_curve(curve)


def normalize_retention_curve(curve: list[Any]) -> list[dict[str, float]]:
    normalized = []

    for point in curve:
        if not isinstance(point, dict):
            continue

        try:
            second = float(point.get("second"))
            retention = float(point.get("retention"))
        except (TypeError, ValueError):
            continue

        normalized.append(
            {
                "second": max(0, second),
                "retention": min(100, max(0, retention)),
            }
        )

    deduped = {}
    for point in normalized:
        deduped[point["second"]] = point["retention"]

    return [
        {"second": second, "retention": retention}
        for second, retention in sorted(deduped.items())
    ]


def select_demo_curve(analysis: dict[str, Any] | None = None) -> list[dict[str, float]]:
    analysis = analysis or {}
    hook_score = _safe_number(analysis.get("hook_score"), 0)
    clarity_score = _safe_number(analysis.get("clarity_score"), 0)
    cta_score = _safe_number(analysis.get("cta_score"), 0)
    average_score = (hook_score + clarity_score + cta_score) / 3

    if hook_score >= 8 and average_score >= 7:
        return [point.copy() for point in STRONG_DEMO_CURVE]
    if hook_score >= 5 and average_score >= 5:
        return [point.copy() for point in AVERAGE_DEMO_CURVE]
    return [point.copy() for point in WEAK_DEMO_CURVE]


def analyze_retention(
    retention_curve: list[dict[str, float]] | None = None,
    analysis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    curve = normalize_retention_curve(retention_curve or []) or select_demo_curve(analysis)

    first_3 = round(_retention_at(curve, 3))
    first_5 = round(_retention_at(curve, 5))
    first_10 = round(_retention_at(curve, 10))
    hook_status = "Strong" if first_5 >= 65 else "Weak"
    useless_viewership_flag = first_10 < 45
    major_dropoffs = _detect_major_dropoffs(curve)
    biggest_dropoff = _biggest_dropoff(curve, major_dropoffs)
    retention_score = _calculate_retention_score(first_3, first_5, first_10, curve)

    engagement_vacancies = _engagement_vacancies(
        first_3=first_3,
        first_5=first_5,
        first_10=first_10,
        major_dropoffs=major_dropoffs,
    )
    recommendations = _recommendations(
        hook_status=hook_status,
        useless_viewership_flag=useless_viewership_flag,
        first_3=first_3,
        first_10=first_10,
        major_dropoffs=major_dropoffs,
    )

    return {
        "retention_score": retention_score,
        "hook_status": hook_status,
        "useless_viewership_flag": useless_viewership_flag,
        "first_3_seconds_retention": first_3,
        "first_5_seconds_retention": first_5,
        "first_10_seconds_retention": first_10,
        "retention_curve": _display_curve(curve),
        "biggest_dropoff": biggest_dropoff,
        "major_dropoffs": major_dropoffs,
        "engagement_vacancies": engagement_vacancies,
        "recommendations": recommendations,
        "verdict": _verdict(retention_score, hook_status, useless_viewership_flag),
    }


def _safe_number(value: Any, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _retention_at(curve: list[dict[str, float]], second: float) -> float:
    seconds = [point["second"] for point in curve]
    index = bisect_left(seconds, second)

    if index < len(curve) and curve[index]["second"] == second:
        return curve[index]["retention"]
    if index == 0:
        return curve[0]["retention"]
    if index >= len(curve):
        return curve[-1]["retention"]

    before = curve[index - 1]
    after = curve[index]
    span = after["second"] - before["second"]
    if span <= 0:
        return after["retention"]

    progress = (second - before["second"]) / span
    return before["retention"] + ((after["retention"] - before["retention"]) * progress)


def _calculate_retention_score(
    first_3: float,
    first_5: float,
    first_10: float,
    curve: list[dict[str, float]],
) -> int:
    end_retention = curve[-1]["retention"] if curve else first_10
    score = (first_3 * 0.1) + (first_5 * 0.25) + (first_10 * 0.5) + (end_retention * 0.15)
    return round(min(100, max(0, score)))


def _detect_major_dropoffs(curve: list[dict[str, float]]) -> list[dict[str, Any]]:
    dropoffs = []

    for previous, current in zip(curve, curve[1:]):
        drop_percent = round(previous["retention"] - current["retention"])
        if drop_percent <= 20:
            continue

        dropoffs.append(
            {
                "timestamp": _format_timestamp(current["second"]),
                "drop_percent": drop_percent,
                "severity": "High" if drop_percent >= 25 else "Medium",
                "reason": _dropoff_reason(previous["second"], current["second"], drop_percent),
            }
        )

    return dropoffs


def _biggest_dropoff(
    curve: list[dict[str, float]],
    major_dropoffs: list[dict[str, Any]],
) -> dict[str, Any] | None:
    drops = []
    for previous, current in zip(curve, curve[1:]):
        drops.append(
            {
                "timestamp": _format_timestamp(current["second"]),
                "drop_percent": round(previous["retention"] - current["retention"]),
                "severity": "High" if previous["retention"] - current["retention"] > 20 else "Medium",
                "reason": _dropoff_reason(previous["second"], current["second"], previous["retention"] - current["retention"]),
            }
        )

    if not drops:
        return None

    biggest = max(drops, key=lambda item: (item["drop_percent"], _timestamp_seconds(item["timestamp"])))
    if major_dropoffs:
        biggest["severity"] = "High" if biggest["drop_percent"] > 20 else "Medium"
    return biggest


def _engagement_vacancies(
    first_3: float,
    first_5: float,
    first_10: float,
    major_dropoffs: list[dict[str, Any]],
) -> list[str]:
    vacancies = []

    if first_3 < 75:
        vacancies.append("Opening hook is not strong enough in the first 3 seconds")
    if first_5 < 65:
        vacancies.append("No strong pattern interrupt in the first 5 seconds")
    if first_10 < 45:
        vacancies.append("Product benefit appears too late for cold viewers")
    if major_dropoffs:
        vacancies.append("Visual pacing slows before viewers have a strong reason to stay")

    if not vacancies:
        vacancies.append("Retention is healthy; keep testing small pacing and CTA variations")

    return vacancies


def _recommendations(
    hook_status: str,
    useless_viewership_flag: bool,
    first_3: float,
    first_10: float,
    major_dropoffs: list[dict[str, Any]],
) -> list[str]:
    recommendations = []

    if first_3 < 75:
        recommendations.append("Show the product result within the first 2 seconds.")
        recommendations.append("Add a bold text overlay that states the main pain point immediately.")
    if hook_status == "Weak":
        recommendations.append("Cut the intro by 3-5 seconds.")
    if first_10 < 45:
        recommendations.append("Move the clearest product benefit before second 8.")
    if useless_viewership_flag or major_dropoffs:
        recommendations.append("Insert a fast visual change before second 8.")

    if not recommendations:
        recommendations.append("Keep the opening structure and test a stronger CTA variation.")

    return recommendations


def _verdict(retention_score: int, hook_status: str, useless_viewership_flag: bool) -> str:
    if retention_score < 50:
        return "This ad loses too much viewer attention in the first 10 seconds, so much of the viewership is low-value."
    if hook_status == "Weak" or useless_viewership_flag:
        return "This ad has useful elements, but the early pacing needs work before scaling spend."
    return "This ad holds attention well enough to keep testing and optimize around the offer and CTA."


def _dropoff_reason(start_second: float, end_second: float, drop_percent: float) -> str:
    if end_second <= 5:
        return "The intro loses viewers before the product value is clear."
    if end_second <= 10:
        return "The ad loses momentum before the product benefit is clearly shown."
    if drop_percent >= 25:
        return "Viewer interest drops sharply after the initial hook."
    return "Pacing slows before a new reason to keep watching appears."


def _format_timestamp(seconds: float) -> str:
    rounded = round(seconds)
    return f"{rounded // 60}:{rounded % 60:02d}"


def _timestamp_seconds(timestamp: str) -> int:
    minutes, seconds = timestamp.split(":")
    return (int(minutes) * 60) + int(seconds)


def _display_curve(curve: list[dict[str, float]]) -> list[dict[str, int]]:
    return [
        {
            "second": round(point["second"]),
            "retention": round(point["retention"]),
        }
        for point in curve
    ]
