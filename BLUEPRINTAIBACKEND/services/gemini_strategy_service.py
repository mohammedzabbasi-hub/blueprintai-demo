import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv, dotenv_values
from google import genai

from services.ai_strategy_writer import write_strategy_summary
from services.pattern_engine import analyze_patterns, detect_shop_issues
from services.metrics_calculator import calculate_shop_totals


BACKEND_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BACKEND_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_env_value(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key) or dotenv_values(ENV_PATH).get(key) or default


def get_gemini_client() -> genai.Client:
    api_key = get_env_value("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(f"GEMINI_API_KEY is missing. Checked: {ENV_PATH}")
    return genai.Client(api_key=api_key)


def slim_engine_payload(creatives: List[Any], product_name: Optional[str] = None) -> Dict[str, Any]:
    totals = calculate_shop_totals(creatives)
    patterns = analyze_patterns(creatives)
    issues = detect_shop_issues(creatives)

    return {
        "product_name": product_name,
        "totals": totals,
        "best_hook": patterns.get("best_hook"),
        "worst_hook": patterns.get("worst_hook"),
        "best_creator_type": patterns.get("best_creator_type"),
        "best_visual_style": patterns.get("best_visual_style"),
        "best_product_angle": patterns.get("best_product_angle"),
        "issues": issues[:8],
        "coded_strategy": write_strategy_summary(creatives),
    }


def build_strategy_prompt(payload: Dict[str, Any]) -> str:
    return f"""
You are BluePrintAI, a TikTok Shop creative strategist.

Use ONLY this engine data.
Do not invent metrics.
Do not judge ROAS if revenue and ad spend are 0.
Return valid JSON only.

JSON structure:
{{
  "executive_summary": "string",
  "main_strengths": ["string", "string", "string"],
  "main_weaknesses": ["string", "string", "string"],
  "top_3_recommendations": [
    {{
      "title": "string",
      "why_it_matters": "string",
      "action_step": "string",
      "priority": "High/Medium/Low"
    }}
  ],
  "next_3_creative_tests": [
    {{
      "test_name": "string",
      "hook": "string",
      "creator_type": "string",
      "visual_style": "string",
      "cta": "string",
      "goal": "string"
    }}
  ]
}}

ENGINE DATA:
{json.dumps(payload, indent=2, default=str)}
"""


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    cleaned = (text or "").strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return None
    return None


def generate_gemini_strategy(creatives: List[Any], product_name: Optional[str] = None) -> Dict[str, Any]:
    payload = slim_engine_payload(creatives, product_name)
    prompt = build_strategy_prompt(payload)

    client = get_gemini_client()
    model = get_env_value("GEMINI_MODEL", "gemini-2.5-flash")

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    raw_text = response.text or ""
    parsed_json = extract_json_from_text(raw_text)

    return {
        "model": model,
        "parsed": parsed_json is not None,
        "gemini_json": parsed_json,
        "gemini_text": raw_text,
        "engine_payload": payload,
    }
