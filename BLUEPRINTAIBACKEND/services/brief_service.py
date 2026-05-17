import json
import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session

load_dotenv(dotenv_path=".env")


def clean_json_response(text: str):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1).strip()

    if text.startswith("```"):
        text = text.replace("```", "", 1).strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return json.loads(text)


def generate_brief(db: Session, shop_id: int, product_name: str, brand_name: str | None = None):
    product = product_name.strip()
    brand = (brand_name or "Your Brand").strip()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from .env")

    client = genai.Client(api_key=api_key)
    model = os.getenv("ANALYSIS_MODEL", "gemini-2.0-flash")

    prompt = f"""
Create a TikTok Shop ad brief for this product.

Product: {product}
Brand: {brand}

Return ONLY valid JSON with these exact fields:
product, brief_title, hook, creator_type, tone, cta, target_audience,
primary_angle, secondary_angle, structure, reasoning, script, shot_list,
dos, donts, references.

Make the brief specific, creator-friendly, TikTok-native, and ready to film.
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        },
    )

    brief = clean_json_response(response.text)

    required_defaults = {
        "product": product,
        "brief_title": f"{brand} {product} TikTok Shop Ad Brief",
        "hook": "Show the product solving a clear problem in the first three seconds.",
        "creator_type": "UGC creator",
        "tone": "Direct, energetic, TikTok-native",
        "cta": "Tap the TikTok Shop link to try it.",
        "target_audience": "TikTok shoppers looking for useful products with creator proof.",
        "primary_angle": f"Show why {brand} {product} is worth buying.",
        "secondary_angle": "Use creator proof, close-up product shots, and a clear CTA.",
        "structure": "Hook → product reveal → demo → proof → CTA",
        "reasoning": "Generated using TikTok Shop creative best practices.",
        "script": "Here is why I switched to this product...",
        "shot_list": "Hook shot\nProduct close-up\nDemo shot\nProof shot\nCTA shot",
        "dos": "Show the product early\nUse natural creator language\nKeep pacing fast",
        "donts": "Do not make it feel like a traditional commercial\nDo not delay the product reveal",
        "references": "TikTok Shop UGC ad structure",
    }

    for key, value in required_defaults.items():
        brief.setdefault(key, value)

    brief["id"] = None
    return brief
