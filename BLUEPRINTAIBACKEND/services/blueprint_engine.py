import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List
# Ensure SQLAlchemy relationship models are registered
import models.video_analysis


from dotenv import load_dotenv
from sqlalchemy.orm import Session

from models.revenue_blueprint import RevenueBlueprint, RevenueBlueprintStep

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_PATH = BASE_DIR / "data" / "blueprint_templates" / "blueprint_rules.json"
STEPS_PATH = BASE_DIR / "data" / "blueprint_templates" / "step_templates.json"


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def safe_float(value, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def empty_metrics() -> Dict[str, Any]:
    return {
        "views": 0,
        "clicks": 0,
        "orders": 0,
        "revenue": 0,
        "ctr": 0,
        "conversion_rate": 0,
        "roas": 0,
        "creatives": 0,
    }


def get_shop_metrics(db: Session, shop_id: int) -> Dict[str, Any]:
    try:
        from models.creative import Creative
        from models.metric import Metric
    except Exception:
        return empty_metrics()

    creatives = db.query(Creative).filter(Creative.shop_id == shop_id).all()
    creative_ids = [creative.id for creative in creatives]

    if not creative_ids:
        return empty_metrics()

    metrics = db.query(Metric).filter(Metric.creative_id.in_(creative_ids)).all()

    total_views = sum(getattr(metric, "views", 0) or 0 for metric in metrics)
    total_clicks = sum(getattr(metric, "clicks", 0) or 0 for metric in metrics)
    total_orders = sum(getattr(metric, "orders", 0) or 0 for metric in metrics)

    total_revenue = 0.0
    for metric in metrics:
        for field in ["revenue", "total_revenue"]:
            if hasattr(metric, field):
                total_revenue += safe_float(getattr(metric, field, 0))

    ctr = (total_clicks / total_views * 100) if total_views else 0
    conversion_rate = (total_orders / total_clicks * 100) if total_clicks else 0

    roas_values = []
    for metric in metrics:
        if hasattr(metric, "roas"):
            value = safe_float(getattr(metric, "roas", 0))
            if value > 0:
                roas_values.append(value)

    avg_roas = sum(roas_values) / len(roas_values) if roas_values else 0

    return {
        "views": total_views,
        "clicks": total_clicks,
        "orders": total_orders,
        "revenue": round(total_revenue, 2),
        "ctr": round(ctr, 2),
        "conversion_rate": round(conversion_rate, 2),
        "roas": round(avg_roas, 2),
        "creatives": len(creatives),
    }


def diagnose_shop(metrics: Dict[str, Any]) -> Dict[str, str]:
    rules_data = load_json(RULES_PATH)
    thresholds = rules_data.get("thresholds", {})

    low_ctr = thresholds.get("low_ctr", 1.5)
    low_conversion_rate = thresholds.get("low_conversion_rate", 1.0)
    low_roas = thresholds.get("low_roas", 1.5)
    low_views = thresholds.get("low_views", 1000)

    ctr = safe_float(metrics.get("ctr"))
    conversion_rate = safe_float(metrics.get("conversion_rate"))
    roas = safe_float(metrics.get("roas"))
    views = safe_float(metrics.get("views"))

    if views < low_views:
        return {
            "main_goal": "Increase reach and creative testing volume",
            "diagnosis": "Your shop does not have enough reach yet, so the first priority is creating more testable TikTok Shop ad variations.",
            "estimated_impact": "More creative testing gives the shop a better chance of finding winning hooks and scalable ad angles.",
        }

    if ctr < low_ctr:
        return {
            "main_goal": "Increase click-through rate",
            "diagnosis": "Your biggest bottleneck appears to be attention. Viewers may not be stopping, watching, or clicking enough.",
            "estimated_impact": "Improving hooks and pacing can increase CTR and create more qualified traffic.",
        }

    if conversion_rate < low_conversion_rate:
        return {
            "main_goal": "Increase conversion rate",
            "diagnosis": "Your ads are getting clicks, but not enough shoppers are converting into buyers.",
            "estimated_impact": "Improving product demos, offer clarity, and CTAs can help turn more clicks into orders.",
        }

    if roas < low_roas:
        return {
            "main_goal": "Improve ROAS and profitability",
            "diagnosis": "Your ads may be generating activity, but the return is not strong enough yet.",
            "estimated_impact": "Testing stronger creators, hooks, and ad briefs can improve profitable scaling.",
        }

    return {
        "main_goal": "Scale winning creative patterns",
        "diagnosis": "Your shop has enough baseline activity to begin improving and scaling the strongest creative patterns.",
        "estimated_impact": "A structured testing loop can help increase revenue, ROAS, and creator efficiency.",
    }


def fallback_steps(metrics: Dict[str, Any], diagnosis: Dict[str, str]) -> List[Dict[str, Any]]:
    templates = load_json(STEPS_PATH)
    base_steps = templates.get("default_steps", [])

    if not base_steps:
        base_steps = [
            {
                "step_number": 1,
                "title": "Diagnose the Main Revenue Bottleneck",
                "description": "Identify the shop's weakest performance area.",
                "action": "Review CTR, conversion rate, ROAS, revenue, and creative volume.",
                "priority": "High",
                "related_feature": "Dashboard",
                "expected_result": "The seller knows what to fix first.",
            }
        ]

    steps = []
    for step in base_steps:
        new_step = dict(step)

        if new_step.get("step_number") == 1:
            new_step["description"] = (
                f"Current shop stats: {metrics.get('views', 0)} views, "
                f"{metrics.get('clicks', 0)} clicks, {metrics.get('orders', 0)} orders, "
                f"{metrics.get('ctr', 0)}% CTR, {metrics.get('conversion_rate', 0)}% conversion rate, "
                f"{metrics.get('roas', 0)} ROAS, and ${metrics.get('revenue', 0)} revenue."
            )
            new_step["action"] = diagnosis["diagnosis"]

        steps.append(new_step)

    return steps


def extract_json_from_ai(text: str):
    cleaned = text.strip()

    cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        return json.loads(match.group(0))

    raise ValueError("AI response did not contain valid JSON.")


def generate_ai_blueprint(metrics: Dict[str, Any], diagnosis: Dict[str, str]) -> Dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in .env")

    import google.generativeai as genai

    genai.configure(api_key=api_key)

    model_name = os.getenv("BLUEPRINT_MODEL", "gemini-2.5-flash-lite")
    model = genai.GenerativeModel(model_name)

    prompt = f"""
You are BluePrintAI, an AI growth strategist for TikTok Shop sellers.

Create a fresh step-by-step TikTok Shop revenue blueprint based on this shop data.

Shop metrics:
- views: {metrics.get("views")}
- clicks: {metrics.get("clicks")}
- orders: {metrics.get("orders")}
- revenue: {metrics.get("revenue")}
- CTR: {metrics.get("ctr")}%
- conversion rate: {metrics.get("conversion_rate")}%
- ROAS: {metrics.get("roas")}
- creatives: {metrics.get("creatives")}

Current diagnosis:
- main_goal: {diagnosis.get("main_goal")}
- diagnosis: {diagnosis.get("diagnosis")}
- estimated_impact: {diagnosis.get("estimated_impact")}

Return ONLY valid JSON with this exact structure:
{{
  "title": "AI Growth Blueprint",
  "main_goal": "...",
  "diagnosis": "...",
  "summary": "...",
  "estimated_impact": "...",
  "steps": [
    {{
      "step_number": 1,
      "title": "...",
      "description": "...",
      "action": "...",
      "priority": "High",
      "related_feature": "Dashboard",
      "expected_result": "..."
    }}
  ]
}}

Rules:
- Create exactly 6 steps.
- Step titles should be short and usable as flowchart box titles.
- Make the steps specific to TikTok Shop ad growth.
- Use features from this app: Dashboard, Video Analysis, Creator Comparison, Ad Briefs, Recommendations.
- Do not mention unsupported features.
- Do not include markdown.
- Do not include commentary outside the JSON.
- Make the wording slightly different each time while staying professional.
"""

    response = model.generate_content(prompt)
    payload = extract_json_from_ai(response.text)

    steps = payload.get("steps", [])
    cleaned_steps = []

    for index, step in enumerate(steps[:6], start=1):
        cleaned_steps.append({
            "step_number": index,
            "title": str(step.get("title", f"Blueprint Step {index}")),
            "description": str(step.get("description", "")),
            "action": str(step.get("action", "")),
            "priority": str(step.get("priority", "Medium")),
            "related_feature": str(step.get("related_feature", "BlueprintAI")),
            "expected_result": str(step.get("expected_result", "")),
        })

    while len(cleaned_steps) < 6:
        cleaned_steps.append({
            "step_number": len(cleaned_steps) + 1,
            "title": "Continue Optimization Loop",
            "description": "Review performance and continue testing the strongest creative direction.",
            "action": "Keep the strongest-performing element and replace the weakest element in the next test.",
            "priority": "Medium",
            "related_feature": "Dashboard",
            "expected_result": "The shop keeps improving through repeated testing.",
        })

    return {
        "title": payload.get("title", "AI Growth Blueprint"),
        "main_goal": payload.get("main_goal", diagnosis["main_goal"]),
        "diagnosis": payload.get("diagnosis", diagnosis["diagnosis"]),
        "summary": payload.get(
            "summary",
            "This blueprint turns shop performance data into a step-by-step TikTok Shop growth plan."
        ),
        "estimated_impact": payload.get("estimated_impact", diagnosis["estimated_impact"]),
        "steps": cleaned_steps,
    }


def generate_blueprint_payload(db: Session, shop_id: int) -> Dict[str, Any]:
    metrics = get_shop_metrics(db, shop_id)
    diagnosis = diagnose_shop(metrics)

    try:
        ai_payload = generate_ai_blueprint(metrics, diagnosis)
        steps = ai_payload["steps"]

        return {
            "shop_id": shop_id,
            "title": ai_payload["title"],
            "main_goal": ai_payload["main_goal"],
            "diagnosis": ai_payload["diagnosis"],
            "summary": ai_payload["summary"],
            "estimated_impact": ai_payload["estimated_impact"],
            "steps": steps,
        }

    except Exception as error:
        print(f"AI blueprint generation failed, using fallback: {error}")

        return {
            "shop_id": shop_id,
            "title": "AI Growth Blueprint",
            "main_goal": diagnosis["main_goal"],
            "diagnosis": diagnosis["diagnosis"],
            "summary": (
                "This blueprint turns your dashboard stats, video analysis, creator comparison, "
                "ad briefs, and recommendations into one step-by-step TikTok Shop growth plan."
            ),
            "estimated_impact": diagnosis["estimated_impact"],
            "steps": fallback_steps(metrics, diagnosis),
        }


def create_blueprint(db: Session, shop_id: int) -> RevenueBlueprint:
    payload = generate_blueprint_payload(db, shop_id)

    blueprint = RevenueBlueprint(
        shop_id=shop_id,
        title=payload["title"],
        main_goal=payload["main_goal"],
        diagnosis=payload["diagnosis"],
        summary=payload["summary"],
        estimated_impact=payload["estimated_impact"],
    )

    db.add(blueprint)
    db.flush()

    for step_data in payload["steps"]:
        step = RevenueBlueprintStep(
            blueprint_id=blueprint.id,
            step_number=step_data["step_number"],
            title=step_data["title"],
            description=step_data["description"],
            action=step_data["action"],
            priority=step_data.get("priority", "Medium"),
            related_feature=step_data.get("related_feature"),
            expected_result=step_data.get("expected_result"),
            is_completed=False,
        )
        db.add(step)

    db.commit()
    db.refresh(blueprint)
    return blueprint


def get_latest_blueprint(db: Session, shop_id: int):
    return (
        db.query(RevenueBlueprint)
        .filter(RevenueBlueprint.shop_id == shop_id)
        .order_by(RevenueBlueprint.created_at.desc())
        .first()
    )


def update_step_completion(db: Session, step_id: int, is_completed: bool):
    step = db.query(RevenueBlueprintStep).filter(RevenueBlueprintStep.id == step_id).first()

    if not step:
        return None

    step.is_completed = is_completed
    db.commit()
    db.refresh(step)
    return step
