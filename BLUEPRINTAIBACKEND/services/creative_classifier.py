from typing import Any, Dict


def _get(obj: Any, key: str, default=""):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _text(creative: Any) -> str:
    fields = [
        "title",
        "caption",
        "transcript",
        "transcript_summary",
        "insight",
        "description",
        "hook",
    ]
    return " ".join(str(_get(creative, f, "")) for f in fields).lower()


def classify_hook_type(creative: Any) -> str:
    text = _text(creative)

    if any(x in text for x in ["problem", "struggle", "tired of", "hate when", "fixes", "solution"]):
        return "Problem/Solution"
    if any(x in text for x in ["watch this", "you won't believe", "secret", "shocking", "i found"]):
        return "Curiosity/Shock"
    if any(x in text for x in ["before", "after", "transformation"]):
        return "Before/After"
    if any(x in text for x in ["review", "honest", "tried", "testing"]):
        return "Review/Testimonial"
    if any(x in text for x in ["how to", "tutorial", "step", "guide"]):
        return "Tutorial"
    if any(x in text for x in ["sale", "discount", "deal", "% off", "limited time"]):
        return "Offer/Discount"

    return _get(creative, "hook_type", "General Product Hook") or "General Product Hook"


def classify_creator_type(creative: Any) -> str:
    text = _text(creative)

    creator_type = _get(creative, "creator_type", "")
    if creator_type:
        return creator_type

    if any(x in text for x in ["doctor", "expert", "dermatologist", "trainer", "specialist"]):
        return "Expert/Educator"
    if any(x in text for x in ["my honest review", "i tried", "testing this"]):
        return "UGC Creator"
    if any(x in text for x in ["customer", "testimonial"]):
        return "Customer Testimonial"
    if any(x in text for x in ["founder", "my brand", "we created"]):
        return "Founder"
    if any(x in text for x in ["asmr", "no talking", "faceless"]):
        return "Faceless Demo"

    return "UGC Creator"


def classify_visual_style(creative: Any) -> str:
    text = _text(creative)

    visual_style = _get(creative, "visual_style", "")
    if visual_style:
        return visual_style

    if any(x in text for x in ["unboxing", "package", "opening"]):
        return "Unboxing"
    if any(x in text for x in ["demo", "demonstration", "showing how"]):
        return "Product Demo"
    if any(x in text for x in ["talking head", "speaking to camera"]):
        return "Talking Head"
    if any(x in text for x in ["pov"]):
        return "POV"
    if any(x in text for x in ["routine", "day in my life", "lifestyle"]):
        return "Lifestyle"
    if any(x in text for x in ["text on screen", "caption heavy"]):
        return "Text-Heavy Edit"

    return "Product Demo"


def classify_cta_type(creative: Any) -> str:
    text = _text(creative)

    if any(x in text for x in ["shop now", "tap to shop", "click the link"]):
        return "Shop Now"
    if any(x in text for x in ["limited time", "before it sells out", "while supplies last"]):
        return "Urgency"
    if any(x in text for x in ["get yours", "grab yours"]):
        return "Get Yours"
    if any(x in text for x in ["discount", "sale", "% off"]):
        return "Discount CTA"

    return _get(creative, "cta_type", "Direct CTA") or "Direct CTA"


def classify_product_angle(creative: Any) -> str:
    text = _text(creative)

    if any(x in text for x in ["save time", "easy", "convenient", "quick"]):
        return "Convenience"
    if any(x in text for x in ["cheap", "affordable", "worth it", "value"]):
        return "Value"
    if any(x in text for x in ["premium", "luxury", "quality"]):
        return "Quality"
    if any(x in text for x in ["pain", "problem", "fix", "solution"]):
        return "Pain Point"
    if any(x in text for x in ["cute", "aesthetic", "style"]):
        return "Aesthetic"

    return "General Product Benefit"


def classify_creative(creative: Any) -> Dict[str, str]:
    return {
        "hook_type": classify_hook_type(creative),
        "creator_type": classify_creator_type(creative),
        "visual_style": classify_visual_style(creative),
        "cta_type": classify_cta_type(creative),
        "product_angle": classify_product_angle(creative),
    }
