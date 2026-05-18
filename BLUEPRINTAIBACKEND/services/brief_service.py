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


def fallback_brief(product: str, brand: str, shop_id: int, error_note: str | None = None):
    return {
        "id": None,
        "product": product,
        "brief_title": f"{brand} {product} TikTok Shop Ad Brief",
        "hook": f"I didn’t expect {product} to make this much of a difference.",
        "creator_type": "UGC creator with a natural, product-demo style",
        "tone": "Fast-paced, honest, creator-led, TikTok-native",
        "cta": "Tap the TikTok Shop link to try it today.",
        "target_audience": "TikTok shoppers who want practical, visually convincing products before buying.",
        "primary_angle": f"Show {product} solving a clear everyday problem in a simple before-and-after format.",
        "secondary_angle": "Use close-up product shots, quick captions, creator reaction, and a direct TikTok Shop CTA.",
        "structure": "Hook → Problem → Product reveal → Demo → Benefit proof → CTA",
        "reasoning": (
            f"This fallback brief was generated from built-in TikTok Shop creative strategy because the AI provider "
            f"was unavailable. Shop ID: {shop_id}."
        ),
        "script": (
            f"Wait, I actually didn’t think {product} would work this well. "
            f"I’ve been looking for something that feels easy to use and actually shows results fast. "
            f"Here’s what I noticed after trying {brand}. First, the product is simple to use. "
            f"Second, you can actually see the difference while I’m using it. "
            f"If you’ve been looking for something like this, check it out through the TikTok Shop link."
        ),
        "shot_list": "0-2s: Creator opens with surprised reaction or bold claim\n2-5s: Show the problem clearly\n5-8s: Product close-up and packaging/product reveal\n8-15s: Demonstrate the product in use\n15-22s: Show result, benefit, or comparison\n22-28s: Creator gives quick honest recommendation\n28-30s: TikTok Shop CTA",
        "dos": "Show the product within the first 3 seconds\nUse captions for every major benefit\nMake the creator sound natural, not scripted\nInclude a clear visual demo\nEnd with a direct TikTok Shop CTA",
        "donts": "Do not make the ad feel like a polished commercial\nDo not wait too long to show the product\nDo not use vague claims without visual proof\nDo not overload the script with too many benefits",
        "references": "TikTok Shop UGC structure\nProblem-solution creative format\nFast hook and product demo framework",
        "fallback": True,
        "error_note": error_note,
    }


def generate_brief(db: Session, shop_id: int, product_name: str, brand_name: str | None = None):
    product = product_name.strip()
    brand = (brand_name or "Your Brand").strip()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return fallback_brief(product, brand, shop_id, "GEMINI_API_KEY is missing.")

    client = genai.Client(api_key=api_key)
    model = os.getenv("ANALYSIS_MODEL", "gemini-2.0-flash")

    prompt = f"""
Create a TikTok Shop ad brief for this product.

Shop ID: {shop_id}
Product: {product}
Brand: {brand}

Return ONLY valid JSON with these exact fields:
product, brief_title, hook, creator_type, tone, cta, target_audience,
primary_angle, secondary_angle, structure, reasoning, script, shot_list,
dos, donts, references.

Make the brief specific, creator-friendly, TikTok-native, and ready to film.
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        brief = clean_json_response(response.text)

    except Exception as e:
        return fallback_brief(product, brand, shop_id, str(e))

    required_defaults = fallback_brief(product, brand, shop_id)
    required_defaults.pop("fallback", None)
    required_defaults.pop("error_note", None)

    for key, value in required_defaults.items():
        brief.setdefault(key, value)

    brief["id"] = None
    brief["fallback"] = False
    return brief
